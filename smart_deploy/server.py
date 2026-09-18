from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from .database import get_project
from .detector import pull_repo, detect_and_deploy

app = FastAPI(title="Smart Deploy Webhook Receiver")

def handle_deployment(project_info: dict):
    """Background task to handle the deployment process."""
    path = project_info.get("path")
    token = project_info.get("token")
    repo_url = project_info.get("repo_url")
    restart_cmd = project_info.get("restart_cmd")

    print(f"--- Initiating deployment pipeline for {repo_url} ---")
    
    if pull_repo(path, token, repo_url):
        detect_and_deploy(path, restart_cmd)
        print("--- Deployment pipeline executed successfully ---")
    else:
        print("--- Deployment pipeline aborted: Pull operation failed ---")

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """Endpoint for receiving GitHub webhook push events."""
    payload = await request.json()
    
    # استخراج نام کامل ریپازیتوری از دیتای ارسالی گیت‌هاب جهت تطبیق با دیتابیس محلی
    try:
        repo_name = payload["repository"]["full_name"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Malformed GitHub payload structure.")

    project_info = get_project(repo_name)
    if not project_info:
        raise HTTPException(status_code=404, detail=f"Repository '{repo_name}' is not registered in Smart Deploy.")

    # اجرای پروسه در پس‌زمینه تا سرور گیت‌هاب با خطای Timeout به دلیل طولانی شدن زمان بیلد مواجه نشود
    background_tasks.add_task(handle_deployment, project_info)
    
    return {"status": "Deployment job queued successfully", "repository": repo_name}