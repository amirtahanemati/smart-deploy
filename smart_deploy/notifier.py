import os
import json
import requests

CONFIG_PATH = os.path.expanduser("~/.smart-deploy/config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def send_notification(message: str):
    config = load_config()
    
    url = config.get("url")
    secret = config.get("secret")
    pairing_code = config.get("pairing_code")
    
    if not all([url, secret, pairing_code]):
        return
        
    payload = {
        "pairing_code": pairing_code,
        "message": message
    }
    
    headers = {
        "Authorization": f"Bearer {secret}",
        "Content-Type": "application/json"
    }
    
    try:
        requests.post(url, json=payload, headers=headers, timeout=5)
    except Exception:
        pass