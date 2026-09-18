import json
from pathlib import Path
from typing import Optional

# تعیین مسیر ذخیره‌سازی اطلاعات پروژه‌ها در دایرکتوری کاربر تا با حذف برنامه دیتابیس پاک نشود
CONFIG_DIR = Path.home() / ".smart-deploy"
DB_FILE = CONFIG_DIR / "projects.json"

def init_db():
    """Initialize the database directory and file if they don't exist."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if not DB_FILE.exists():
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

def load_projects() -> dict:
    """Load all projects from the JSON database."""
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_project(repo_url: str, path: str, token: Optional[str] = None, restart_cmd: Optional[str] = None) -> str:
    """Save a new project to the database and return the extracted repository name."""
    projects = load_projects()
    
    # استخراج شناسه یکتای ریپازیتوری از لینک برای استفاده به عنوان کلید اصلی
    repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
    
    projects[repo_name] = {
        "repo_url": repo_url,
        "path": path,
        "token": token,
        "restart_cmd": restart_cmd
    }
    
    with open(DB_FILE, "w") as f:
        json.dump(projects, f, indent=4)
        
    return repo_name
    
def get_project(repo_name: str) -> Optional[dict]:
    """Retrieve project configuration by repository name."""
    projects = load_projects()
    return projects.get(repo_name)