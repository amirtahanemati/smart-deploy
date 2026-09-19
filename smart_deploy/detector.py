import os
import subprocess
from typing import Optional

def run_command(command: str, cwd: str) -> bool:
    """Execute a shell command in the specified directory and print the output."""
    print(f"Executing: [{command}] in {cwd}", flush=True)
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
            print(f"Success:\n{result.stdout.strip()}", flush=True)
            return True
        else:
            print(f"Error:\n{result.stderr.strip()}", flush=True)
            return False
    except Exception as e:
        print(f"System Exception: {e}", flush=True)
        return False

def detect_and_deploy(path: str, restart_cmd: Optional[str] = None):
    """Analyze the project structure, pull latest code, and run appropriate build commands."""
    print("\n--- Starting Deployment Cycle ---", flush=True)
    
    # مرحله اول: دریافت کدهای جدید از گیت‌هاب
    print("Pulling latest code...", flush=True)
    run_command("git pull", path)
    
    # مرحله دوم: بررسی و بیلد پروژه
    if os.path.exists(os.path.join(path, "package.json")):
        print("Framework detected: Node.js", flush=True)
        run_command("npm install", path)
        
        if os.path.exists(os.path.join(path, "next.config.js")) or os.path.exists(os.path.join(path, "next.config.mjs")):
            print("Framework detected: Next.js", flush=True)
            run_command("npm run build", path)
            
    elif os.path.exists(os.path.join(path, "requirements.txt")):
        print("Framework detected: Python", flush=True)
        pip_cmd = "venv/bin/pip" if os.path.exists(os.path.join(path, "venv")) else "pip"
        run_command(f"{pip_cmd} install -r requirements.txt", path)

    # مرحله سوم: راه‌اندازی مجدد سرویس زنده
    if restart_cmd:
        print(f"Executing custom restart command: {restart_cmd}", flush=True)
        run_command(restart_cmd, path)
    else:
        print("No custom restart command provided. Deployment cycle completed.", flush=True)