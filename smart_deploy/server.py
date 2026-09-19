from fastapi import FastAPI, Request, BackgroundTasks
from .database import get_project, load_projects
from .detector import detect_and_deploy

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    print("\n--- Webhook Received ---")
    try:
        payload = await request.json()
        
        # بررسی اینکه آیا درخواست از نوع پوش (Push) است
        if "ref" not in payload:
            print("Ignored: Not a push event.")
            return {"message": "Ignored: Not a push event"}

        # استخراج نام ریپازیتوری ارسالی از گیت‌هاب
        repo_full_name = payload.get("repository", {}).get("full_name", "")
        print(f"Target Repository: {repo_full_name}")

        # جستجوی پروژه در دیتابیس با استفاده از تابع پایگاه‌داده
        project_data = get_project(repo_full_name)
        
        # در صورتی که به خاطر حروف کوچک/بزرگ پیدا نشد (Fallback)
        if not project_data:
            projects = load_projects()
            for key, val in projects.items():
                if key.lower() == repo_full_name.lower():
                    project_data = val
                    break

        if project_data:
            print(f"Match found! Queuing deployment for {repo_full_name} at {project_data['path']}")
            
            # اجرای دیپلوی در پس‌زمینه با استفاده از تابع صحیح از detector.py
            background_tasks.add_task(
                detect_and_deploy, 
                project_data["path"], 
                project_data.get("restart_cmd")
            )
            return {"message": "Deployment queued"}
        else:
            print(f"Ignored: Repository {repo_full_name} is not registered in smart-deploy.")
            return {"message": "Repository not registered"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": str(e)}