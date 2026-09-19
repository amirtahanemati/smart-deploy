import uvicorn
import typer
import shutil
import getpass
import subprocess
from .database import save_project
from .github_api import setup_webhook

app = typer.Typer(help="Smart Deploy: Automated CI/CD Tool for Developers")

@app.command()
def add(
    repo_url: str = typer.Argument(..., help="Target GitHub Repository URL"),
    path: str = typer.Argument(..., help="Absolute local path on the server"),
    server_url: str = typer.Argument(..., help="Public URL or IP of this server (e.g., http://8.8.8.8:9000)"),
    token: str = typer.Option(None, "--token", "-t", help="GitHub Personal Access Token (requires 'repo' permissions)"),
    restart_cmd: str = typer.Option(None, "--restart", "-r", help="Custom command to run after deployment (e.g., 'pm2 restart api')")
):
    """
    Register a new project and automatically configure its GitHub webhook.
    """
    typer.echo(f"Registering project: {repo_url} at {path}")
    
    # ذخیره کانفیگ پروژه در سیستم جهت ارجاع هنگام دریافت درخواست وب‌هوک
    repo_name = save_project(repo_url, path, token, restart_cmd)
    typer.secho(f"Project '{repo_name}' successfully added to the local database.", fg=typer.colors.GREEN)
    
    # در صورت وجود توکن، ارتباط با گیت‌هاب و ثبت وب‌هوک آغاز می‌شود
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
    """
    Start the background FastAPI server to listen for GitHub webhooks.
    """
    typer.secho(f"Initializing Smart Deploy Listener on port {port}...", fg=typer.colors.CYAN)
    uvicorn.run("smart_deploy.server:app", host="0.0.0.0", port=port)

@app.command()
def generate_service(port: int = typer.Option(9000, "--port", "-p", help="Port number for the webhook listener")):
    """
    Generate a systemd service configuration for Linux servers to run in the background.
    """
    # پیدا کردن مسیر دقیق فایل اجرایی و نام کاربری لینوکس
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
    typer.echo("sudo systemctl daemon-reload")
    typer.echo("sudo systemctl enable smart-deploy")
    typer.echo("sudo systemctl start smart-deploy")
    typer.echo("sudo systemctl status smart-deploy")

if __name__ == "__main__":
    app()