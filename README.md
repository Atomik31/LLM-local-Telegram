# Guide de Démarrage - Bot Telegram + Mistral 7B

## Prérequis
- Python 3.8+
- LM Studio installé et lancé avec Mistral 7B
- Un token Telegram Bot (créé via BotFather)

## Étapes d'installation

### 1. Créer un bot Telegram
1. Ouvre Telegram et recherche "BotFather"
2. Envoie `/start` puis `/newbot`
3. Suis les instructions (donne un nom à ton bot)
4. Tu recevras un token comme : `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Copie ce token

### 2. Configurer le .env
1. Ouvre le fichier `.env`
2. Remplace `YOUR_BOT_TOKEN` par ton vrai token Telegram
3. Vérifie que `LM_STUDIO_URL` = `http://localhost:1234/v1/chat/completions`
4. Vérifie que `MODEL_NAME` = `mistral-7b-instruct-v0.3`

Exemple de .env complété :
```
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
LM_STUDIO_URL=http://localhost:1234/v1/chat/completions
MODEL_NAME=mistral-7b-instruct-v0.3
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Démarrer LM Studio
- Ouvre LM Studio
- Charge le modèle "Mistral 7B Instruct v0.3"
- Lance le serveur local (doit être sur port 1234)
- Attends que le modèle soit chargé

### 5. Lancer le bot
```bash
python bot.py
```

Tu devrais voir dans le terminal : "Bot démarré..."

### 6. Tester le bot
1. Ouvre Telegram et recherche ton bot par son nom
2. Envoie `/start`
3. Envoie un message (ex: "Comment faire une boucle en Python?")
4. Le bot doit répondre en tant qu'expert technique

## Fonctionnalités

- **Conversation persistante** : Le bot se souvient de l'historique (max 20 derniers messages)
- **Historique sauvegardé** : Tous les messages sont sauvegardés dans `history.json`
- **Multi-utilisateurs** : Chaque utilisateur a son propre historique isolé
- **Réinitialisation** : `/start` réinitialise la conversation

## Historique des conversations

Le bot sauvegarde automatiquement toutes les conversations dans `history.json`. Tu peux consulter cet historique directement.

Structure du fichier :
```json
{
  "user_id": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## Dépannage

**Le bot ne répond pas**
- Vérifie que LM Studio tourne et que le modèle est chargé
- Teste manuellement : `http://localhost:1234/v1/models` dans le navigateur
- Vérifie le token Telegram (pas d'espaces)
- Vérifie l'URL dans .env

**Erreur 400**
- Vérifie que le `MODEL_NAME` dans .env correspond exactement au modèle chargé dans LM Studio
- Vérifie que ton prompt/message n'est pas trop long (max 4096 tokens)

**Erreur "Connection refused"**
- LM Studio n'est pas lancé
- Ou il ne tourne pas sur le port 1234
- Relance LM Studio

**Le modèle ne correspond pas**
- Va sur `http://localhost:1234/v1/models` pour voir le nom exact du modèle
- Mets à jour `MODEL_NAME` dans `.env`

## Personnaliser le bot

Modifie `SYSTEM_PROMPT` dans `bot.py` pour changer le rôle du bot.

Exemple actuel (Expert Python/ML/IA) :
```python
SYSTEM_PROMPT = """Tu es un assistant expert en code python, machine learning, deep learning et intelligence artificielle au global.
Tu aides les utilisateurs avec leurs questions techniques en apportant des réponses claires, précises et simples.
Proposes toujours un code simple et compréhensible. 
Sois concis dans tes réponses (max 150 mots)."""
```

Tu peux le changer pour n'importe quel autre rôle.

## Lancer le bot en arrière-plan (Windows)

```bash
start /B python bot.py
```

## Lancer le bot en arrière-plan (Linux/Mac)

```bash
nohup python bot.py > bot.log 2>&1 &
```

C'est prêt à l'emploi!
