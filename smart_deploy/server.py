from fastapi import FastAPI, Request, BackgroundTasks
from .database import get_project, load_projects
from .detector import detect_and_deploy

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    print("\n--- Webhook Received ---")
    try:
        payload = await request.json()
        
        if "ref" not in payload:
            print("Ignored: Not a push event.")
            return {"message": "Ignored: Not a push event"}

        repo_full_name = payload.get("repository", {}).get("full_name", "")
        print(f"Target Repository: {repo_full_name}")

        project_data = get_project(repo_full_name)
        
        if not project_data:
            projects = load_projects()
            for key, val in projects.items():
                if key.lower() == repo_full_name.lower():
                    project_data = val
                    break

        if project_data:
            print(f"Match found! Queuing deployment for {repo_full_name} at {project_data['path']}")
            
            background_tasks.add_task(
                detect_and_deploy, 
                project_data["path"], 
                project_data.get("restart_cmd"),
                project_data.get("proxy")
            )
            return {"message": "Deployment queued"}
        else:
            print(f"Ignored: Repository {repo_full_name} is not registered in smart-deploy.")
            return {"message": "Repository not registered"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": str(e)}