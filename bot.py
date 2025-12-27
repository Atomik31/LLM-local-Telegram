import requests
import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HISTORY_FILE = "history.json"

SYSTEM_PROMPT = """Tu es un assistant expert en code python, machine learning, deep learning et intelligence artificielle au global.
Tu aides les utilisateurs avec leurs questions techniques en apportant des réponses claires, précises et simples.
Proposes toujours un code simple et compréhensible. 
Sois concis dans tes réponses (max 150 mots)."""

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

history = load_history()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    history[user_id] = []
    save_history(history)
    await update.message.reply_text("Bienvenue! Comment puis-je t'aider?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_message = update.message.text
    
    if user_id not in history:
        history[user_id] = []
    
    # Ajouter message utilisateur
    history[user_id].append({"role": "user", "content": user_message})
    
    # Construire les messages pour l'API
    messages = [{"role": "user", "content": SYSTEM_PROMPT}] + history[user_id]
    
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }
    
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        ai_response = response.json()["choices"][0]["message"]["content"]
        
        # Ajouter réponse du bot
        history[user_id].append({"role": "assistant", "content": ai_response})
        
        # Garder max 20 messages
        if len(history[user_id]) > 20:
            history[user_id] = history[user_id][-20:]
        
        save_history(history)
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f"Erreur: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()