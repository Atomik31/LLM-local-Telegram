import requests
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

# Prompt système pour définir le rôle du bot
SYSTEM_PROMPT = """Tu es un assistant de vente pour un e-commerce. 
Tu dois être amical, utile et convaincant.
Aide les clients à trouver les produits qu'ils cherchent, réponds à leurs questions sur les produits et propose des articles similaires.
Sois concis dans tes réponses (max 150 mots)."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bienvenue! Je suis l'assistant de vente. Comment puis-je t'aider?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Construction du payload avec prompt système
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": f"{SYSTEM_PROMPT}\n\n{user_message}"}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }
    
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        ai_response = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(ai_response)
        
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Erreur de connexion: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot démarré et en attente de messages...")
    app.run_polling()

if __name__ == "__main__":
    main()