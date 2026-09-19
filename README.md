# 🚀 Smart Deploy

![PyPI version](https://img.shields.io/pypi/v/smart-deploy?color=blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)

**Smart Deploy** is a lightweight, zero-configuration CI/CD tool designed for independent developers and small teams. It bridges the gap between your GitHub repositories and your Linux server, automating the entire deployment process with a single command.

No complex YAML files. No heavy Jenkins pipelines. Just raw efficiency.

## ✨ Features

- **Zero-Config Webhooks**: Automatically configures GitHub webhooks using your Personal Access Token.
- **Smart Framework Detection**: Automatically detects Node.js (Next.js/React) and Python projects.
- **Auto Dependency Resolution**: Runs `npm install`, `npm run build`, or `pip install` based on your project's ecosystem.
- **Custom Post-Deploy Commands**: Seamlessly integrates with process managers like PM2 or Systemd.
- **Native Systemd Integration**: Includes a built-in command to generate Linux background services.
- **Multi-Project Support**: Manage dozens of projects on a single server with one lightweight background listener.

---

## 📦 Installation

Smart Deploy is published on PyPI, making installation incredibly simple. It is recommended to use `pipx` to install it globally in an isolated environment on your Linux server:

```bash
# Install using pipx (Recommended for Linux servers)
pipx install smart-deploy

# OR install using standard pip
pip install smart-deploy
```

---

## 🚀 Quick Start

### 1. Generate & Start the Background Service

To ensure Smart Deploy runs 24/7 and survives server reboots, run the built-in service generator:

```bash
smart-deploy generate-service --port 9000

```

_Follow the on-screen instructions to create, enable, and start the `systemd` service._

### 2. Prepare Your Server Directory

Ensure the target directory on your server is initialized as a Git repository and connected to your GitHub remote:

```bash
cd /var/www/your-project
git init
git remote add origin https://github.com/YourUsername/your-repo.git
git fetch origin
git branch --set-upstream-to=origin/main main

```

### 3. Register Your Project

Link your GitHub repository to the local directory. Smart Deploy will automatically contact the GitHub API and configure the webhook.

**For Standard/Static Projects (e.g., React, Vite):**

```bash
smart-deploy add https://github.com/YourUsername/your-repo \
  /var/www/your-project \
  http://YOUR_SERVER_IP:9000 \
  --token "ghp_your_github_personal_access_token" \
  --restart "npm run build"

```

**For Next.js / Live Node.js Projects (using PM2):**

```bash
smart-deploy add https://github.com/YourUsername/your-repo \
  /var/www/your-project \
  http://YOUR_SERVER_IP:9000 \
  --token "ghp_your_github_personal_access_token" \
  --restart "npm run build && pm2 restart my-app"

```

**Parameters Explained:**

- `Repo URL`: The target GitHub repository URL.
- `Local Path`: The absolute path to your project on the server (e.g., `/var/www/your-project`).
- `Server URL`: Your server's public IP/Domain and the port (e.g., `http://123.45.67.89:9000`).
- `--token`: Your GitHub Personal Access Token (requires `repo` and `admin:repo_hook` permissions).
- `--restart`: (Optional) The command to run after pulling and building the code.

### 4. Push and Relax

Now, simply push your code from your local machine:

```bash
git commit -m "feat: awesome new feature"
git push

```

Smart Deploy will intercept the webhook, pull the latest code, install dependencies, build the project, and restart the service automatically.
You can monitor the live deployment logs on your server using:

```bash
sudo journalctl -u smart-deploy.service -f

```

---

## 🧠 How the Smart Detector Works

When a push webhook is triggered, Smart Deploy analyzes the target directory on your server:

1. **Pull Code:** Executes `git pull` to fetch the latest commits.
2. **Node.js / Next.js**: If `package.json` is found, it executes `npm install`. If `next.config.js` or `next.config.mjs` is also present, it proceeds with `npm run build`.
3. **Python**: If `requirements.txt` is found, it automatically locates your virtual environment (`venv`) and runs `pip install -r requirements.txt`.
4. **Custom Execution**: Finally, it runs the custom `--restart` command provided during the `add` step.

---

## 🛠️ CLI Commands Reference

- `smart-deploy add`: Register a new project and set up webhooks automatically.
- `smart-deploy start`: Launch the FastAPI webhook receiver directly in the terminal (for testing).
- `smart-deploy generate-service`: Generate a systemd unit file for production background execution.
- `smart-deploy --help`: View the detailed help menu.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

Developed with ❤️ by [Amirtaha Nemati](https://github.com/amirtahanemati).
