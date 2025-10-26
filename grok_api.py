import os
import requests
from dotenv import load_dotenv

# Charge la clé depuis .env
load_dotenv()
API_KEY = os.getenv("GROK_API_KEY")

def ask_grok(prompt):
    if not API_KEY:
        return "Erreur : GROK_API_KEY manquante dans .env"
    
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "grok-beta",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erreur Grok : {str(e)}"