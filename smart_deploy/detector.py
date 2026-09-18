import os
import subprocess
from typing import Optional

def run_command(command: str, cwd: str) -> bool:
    """Execute a shell command in the specified directory and print the output."""
    print(f"Executing: [{command}] in {cwd}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            print(f"Success:\n{result.stdout.strip()}")
            return True
        else:
            print(f"Error:\n{result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"System Exception: {e}")
        return False

def pull_repo(path: str, token: Optional[str], repo_url: str) -> bool:
    """Pull the latest changes from the remote repository."""
    if token:
        # تزریق مستقیم توکن به آدرس ریپازیتوری برای دور زدن نیاز به احراز هویت تعاملی در سرور
        url_without_protocol = repo_url.replace("https://", "")
        auth_url = f"https://{token}@{url_without_protocol}"
        run_command(f"git remote set-url origin {auth_url}", path)
    
    return run_command("git pull", path)

def detect_and_deploy(path: str, restart_cmd: Optional[str] = None):
    """Analyze the project structure and run appropriate build commands."""
    
    # بررسی وجود فایل‌های پایه جاوا اسکریپت برای تشخیص فریم‌ورک‌های مبتنی بر Node
    if os.path.exists(os.path.join(path, "package.json")):
        print("Framework detected: Node.js")
        run_command("npm install", path)
        
        if os.path.exists(os.path.join(path, "next.config.js")) or os.path.exists(os.path.join(path, "next.config.mjs")):
            print("Framework detected: Next.js")
            run_command("npm run build", path)
            
    # بررسی ساختار پروژه‌های پایتونی
    elif os.path.exists(os.path.join(path, "requirements.txt")):
        print("Framework detected: Python")
        # اولویت استفاده از محیط مجازی در صورت وجود برای جلوگیری از تداخل پکیج‌ها در سرور
        pip_cmd = "venv/bin/pip" if os.path.exists(os.path.join(path, "venv")) else "pip"
        run_command(f"{pip_cmd} install -r requirements.txt", path)

    # اجرای دستور ری‌استارت شخصی‌سازی شده در صورت تعریف توسط کاربر
    if restart_cmd:
        print(f"Executing custom restart command: {restart_cmd}")
        run_command(restart_cmd, path)
    else:
        print("No custom restart command provided. Deployment cycle completed.")