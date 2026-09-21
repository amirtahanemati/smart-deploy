import os
import requests
from dotenv import load_dotenv
from .database import get_pairing_code

load_dotenv()

CENTRAL_BOT_URL = os.getenv("CENTRAL_BOT_URL", "https://bot.tahanemati.ir/api/notify")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "default_secret_key") 

def send_notification(message: str):
    """Push deployment logs to the central Telegram bot server."""
    pairing_code = get_pairing_code()
    
    if not pairing_code:
        return
        
    payload = {
        "pairing_code": pairing_code,
        "message": message
    }
    
    headers = {
        "Authorization": f"Bearer {WEBHOOK_SECRET}",
        "Content-Type": "application/json"
    }
    
    proxies = {
        "http": None,
        "https": None
    }
    
    try:
        requests.post(CENTRAL_BOT_URL, json=payload, headers=headers, proxies=proxies, timeout=5)
    except Exception as e:
        print(f"Failed to push log to central bot server: {e}", flush=True)