import json
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".smart-deploy"
DB_FILE = CONFIG_DIR / "projects.json"

def init_db():
    """Initialize the database directories and files if they don't exist."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if not DB_FILE.exists():
        with open(DB_FILE, "w") as f:
            json.dump({}, f)

# --- Project Management ---
def load_projects() -> dict:
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_project(
    repo_url: str, 
    path: str, 
    token: Optional[str] = None, 
    restart_cmd: Optional[str] = None, 
    proxy: Optional[str] = None
) -> str:
    projects = load_projects()
    repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
    
    projects[repo_name] = {
        "repo_url": repo_url,
        "path": path,
        "token": token,
        "restart_cmd": restart_cmd,
        "proxy": proxy
    }
    with open(DB_FILE, "w") as f:
        json.dump(projects, f, indent=4)
    return repo_name
    
def get_project(repo_name: str) -> Optional[dict]:
    projects = load_projects()
    return projects.get(repo_name)