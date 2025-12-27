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
4. Vérifie que `MODEL_NAME` correspond à ton modèle dans LM Studio

Exemple de .env complété :
```
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
LM_STUDIO_URL=http://localhost:1234/v1/chat/completions
MODEL_NAME=mistral-7b-0.3
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Démarrer LM Studio
- Ouvre LM Studio
- Charge le modèle "Mistral 7B 0.3"
- Lance le serveur local (doit être sur port 1234)
- Attends que le modèle soit chargé

### 5. Lancer le bot
```bash
python bot.py
```

Tu devrais voir dans le terminal : "Bot démarré et en attente de messages..."

### 6. Tester le bot
1. Ouvre Telegram et recherche ton bot par son nom
2. Envoie `/start`
3. Envoie un message (ex: "Recommande-moi un produit")
4. Le bot doit répondre via Mistral 7B

## Dépannage

**Le bot ne répond pas**
- Vérifie que LM Studio tourne et que le modèle est chargé
- Teste manuellement : `http://localhost:1234/v1/models` dans le navigateur
- Vérifie le token Telegram (pas d'espaces)
- Vérifie l'URL dans .env

**Erreur "Connection refused"**
- LM Studio n'est pas lancé
- Ou il ne tourne pas sur le port 1234
- Relance LM Studio

**Le modèle ne correspond pas**
- Dans LM Studio, clique sur le modèle pour voir son nom exact
- Mets à jour `MODEL_NAME` dans `.env`

## Personnaliser le bot

Tu peux modifier le rôle du bot en changeant `SYSTEM_PROMPT` dans `bot.py`

Exemples :

**Support client :**
```python
SYSTEM_PROMPT = """Tu es un agent de support client professionnel.
Aide les utilisateurs à résoudre leurs problèmes rapidement.
Sois empathique et propose des solutions concrètes."""
```

**Assistant général :**
```python
SYSTEM_PROMPT = """Tu es un assistant IA utile et amical.
Réponds aux questions de manière claire et concise."""
```

## Lancer le bot en arrière-plan (Windows)

```bash
start /B python bot.py
```

## Lancer le bot en arrière-plan (Linux/Mac)

```bash
nohup python bot.py > bot.log 2>&1 &
```

C'est prêt à l'emploi!
