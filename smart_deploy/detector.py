import os
import subprocess
import time
from typing import Optional
from .notifier import send_notification

def run_command(command: str, cwd: str) -> str:
    """Execute a shell command, raise an exception on failure to trigger rollback."""
    print(f"Executing: [{command}] in {cwd}", flush=True)
    result = subprocess.run(
        command, 
        shell=True, 
        cwd=cwd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    if result.returncode != 0:
        error_msg = result.stderr.strip() or result.stdout.strip()
        print(f"Command Error:\n{error_msg}", flush=True)
        raise RuntimeError(f"Command failed: {command}\n{error_msg}")
    
    success_msg = result.stdout.strip()
    print(f"Success:\n{success_msg}", flush=True)
    return success_msg

def detect_and_deploy(path: str, restart_cmd: Optional[str] = None):
    """Manage the deployment lifecycle, install dependencies, and handle rollbacks."""
    print("\n--- Starting Deployment Cycle ---", flush=True)
    start_time = time.time()
    repo_name = os.path.basename(path.rstrip('/'))
    
    send_notification(f"🚀 <b>Deployment Started</b>\nRepository: <code>{repo_name}</code>")
    
    # 1. Record the current healthy state for potential rollback
    try:
        current_commit = run_command("git rev-parse HEAD", path).strip()
    except Exception:
        current_commit = None
        print("Warning: Could not fetch current commit hash.", flush=True)

    try:
        # 2. Pull latest code
        print("Pulling latest code...", flush=True)
        run_command("git pull", path)
        
        # 3. Detect framework and build
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

        # 4. Restart service
        if restart_cmd:
            print(f"Executing custom restart command: {restart_cmd}", flush=True)
            run_command(restart_cmd, path)
        else:
            print("No custom restart command provided.", flush=True)
            
        duration = round(time.time() - start_time, 2)
        send_notification(f"✅ <b>Deployment Successful</b>\nRepository: <code>{repo_name}</code>\nTime: {duration}s")

    except Exception as e:
        # 5. Rollback Mechanism
        error_summary = str(e)[:400]
        rollback_msg = ""
        
        if current_commit:
            print("Initiating rollback procedure...", flush=True)
            try:
                run_command(f"git reset --hard {current_commit}", path)
                if restart_cmd:
                    run_command(restart_cmd, path)
                rollback_msg = "\n\n⚠️ <b>System Rolled Back</b> to the previous healthy state."
                print("Rollback successful.", flush=True)
            except Exception as rollback_err:
                rollback_msg = f"\n\n❌ <b>CRITICAL: Rollback Failed!</b>\n{str(rollback_err)[:200]}"
                print("Rollback failed!", flush=True)
        
        duration = round(time.time() - start_time, 2)
        send_notification(
            f"❌ <b>Deployment Failed</b>\nRepository: <code>{repo_name}</code>\nTime: {duration}s\n\n<b>Error:</b>\n<code>{error_summary}</code>{rollback_msg}"
        )