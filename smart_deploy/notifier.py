import requests
from .database import get_pairing_code

# Centralized Bot API Endpoint
CENTRAL_BOT_URL = "https://bot.tahanemati.ir/api/notify"
# Must match the WEBHOOK_SECRET in your central bot configuration
WEBHOOK_SECRET = "super_secret_key_for_clients" 

def send_notification(message: str):
    """Push deployment logs to the central Telegram bot server."""
    pairing_code = get_pairing_code()
    
    # Silently skip if the user hasn't paired their server yet
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
    
    try:
        requests.post(CENTRAL_BOT_URL, json=payload, headers=headers, timeout=5)
    except Exception as e:
        print(f"Failed to push log to central bot server: {e}", flush=True)