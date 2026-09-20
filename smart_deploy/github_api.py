import requests

def setup_webhook(repo_name: str, token: str, server_url: str) -> bool:
    """Configure a push webhook on the target GitHub repository."""
    api_url = f"https://api.github.com/repos/{repo_name}/hooks"
    target_webhook_url = f"{server_url}/webhook"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "name": "web",
        "active": True,
        "events": ["push"],
        "config": {
            "url": target_webhook_url,
            "content_type": "json",
            "insecure_ssl": "1" # Allow insecure SSL for testing servers
        }
    }
    
    # Check existing webhooks to prevent duplicates
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            for hook in response.json():
                if hook.get("config", {}).get("url") == target_webhook_url:
                    print(f"Webhook configuration already exists for {target_webhook_url}")
                    return True
    except Exception as e:
        print(f"Failed to fetch existing webhooks: {e}")
        
    # Register the new webhook
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 201:
            print("Webhook successfully registered on GitHub.")
            return True
        else:
            print(f"Webhook registration failed [{response.status_code}]: {response.text}")
            return False
    except Exception as e:
        print(f"Exception occurred during webhook registration: {e}")
        return False