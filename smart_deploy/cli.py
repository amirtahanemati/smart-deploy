import uvicorn
import typer
import shutil
import getpass
import base64
import json
import os
import sys
from .database import save_project
from .github_api import setup_webhook

app = typer.Typer(help="Smart Deploy: Automated CI/CD Tool for Developers")
bot_app = typer.Typer(help="Manage Telegram Bot Integration")
app.add_typer(bot_app, name="bot")

CONFIG_DIR = os.path.expanduser("~/.smart-deploy")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

@bot_app.command("link")
def bot_link(
    token: str = typer.Argument(..., help="The base64 magic token provided by the central Telegram bot")
):
    """Securely link this server to the central Telegram bot using a generated token."""
    try:
        # Decode the Base64 token
        decoded_bytes = base64.b64decode(token)
        config_data = json.loads(decoded_bytes.decode('utf-8'))
        
        # Validate the data structure
        required_keys = ("url", "secret", "pairing_code")
        if not all(k in config_data for k in required_keys):
            typer.secho("❌ Error: Invalid token structure. Missing required security fields.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        # Create the hidden directory and config file
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        # Save the configuration securely
        with open(CONFIG_PATH, "w") as f:
            json.dump(config_data, f, indent=4)
            
        typer.secho("\n✅ Server Successfully Linked to Telegram Bot!", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"🔗 Pairing Code: {config_data['pairing_code']}\n")
        
    except Exception as e:
        typer.secho("❌ Error parsing token. Please ensure you copied the entire base64 string provided by the bot.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def add(
    repo_url: str = typer.Argument(..., help="Target GitHub Repository URL"),
    path: str = typer.Argument(..., help="Absolute local path on the server"),
    server_url: str = typer.Argument(..., help="Public URL or IP of this server"),
    token: str = typer.Option(None, "--token", "-t", help="GitHub Personal Access Token"),
    restart_cmd: str = typer.Option(None, "--restart", "-r", help="Custom restart command"),
    proxy: str = typer.Option(None, "--proxy", "-x", help="Local proxy URL (e.g., http://127.0.0.1:10808)")
):
    """Register a new project and automatically configure its GitHub webhook."""
    typer.echo(f"Registering project: {repo_url} at {path}")
    if proxy:
        typer.echo(f"Proxy configured for deployments: {proxy}")
    
    repo_name = save_project(repo_url, path, token, restart_cmd, proxy)
    typer.secho(f"Project '{repo_name}' successfully added to the local database.", fg=typer.colors.GREEN)
    
    if token:
        typer.echo("Initiating automated GitHub webhook configuration...")
        if setup_webhook(repo_name, token, server_url):
            typer.secho("GitHub Webhook configured successfully.", fg=typer.colors.GREEN)
        else:
            typer.secho("Failed to configure GitHub Webhook. Verify token permissions.", fg=typer.colors.RED)
    else:
        typer.secho("Warning: No token provided. Automated webhook configuration skipped.", fg=typer.colors.YELLOW)

@app.command()
def start(port: int = typer.Option(9000, "--port", "-p", help="Port number for the webhook listener")):
    """Start the background FastAPI server to listen for GitHub webhooks."""
    typer.secho(f"Initializing Smart Deploy Listener on port {port}...", fg=typer.colors.CYAN)
    uvicorn.run("smart_deploy.server:app", host="0.0.0.0", port=port)

@app.command()
def generate_service(port: int = typer.Option(9000, "--port", "-p", help="Port number for the webhook listener")):
    """Generate a systemd service configuration for Linux servers."""
    executable = shutil.which("smart-deploy") or "/usr/local/bin/smart-deploy"
    user = getpass.getuser()
    
    service_content = f"""[Unit]
Description=Smart Deploy Webhook Listener
After=network.target

[Service]
User={user}
ExecStart={executable} start --port {port}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
    
    typer.secho("1. Create a new service file using nano:", fg=typer.colors.CYAN)
    typer.echo("sudo nano /etc/systemd/system/smart-deploy.service\n")
    typer.secho("2. Paste the following configuration into the file:\n", fg=typer.colors.CYAN)
    typer.echo(service_content)
    typer.secho("3. Enable and start the service by running:", fg=typer.colors.YELLOW)
    typer.echo("sudo systemctl daemon-reload\nsudo systemctl enable smart-deploy\nsudo systemctl start smart-deploy\nsudo systemctl status smart-deploy")

if __name__ == "__main__":
    app()