# 🚀 Smart Deploy

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/amirtahanemati/smart-deploy/python-package.yml?branch=main)
![PyPI version](https://img.shields.io/pypi/v/smart-deploy?color=blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)

**Smart Deploy** is a lightweight, zero-configuration CI/CD tool designed for independent developers and small teams. It bridges the gap between your GitHub repositories and your Linux server, automating the entire deployment process with a single command.

No complex YAML files. No heavy Jenkins pipelines. No manual `.env` configurations. Just raw efficiency.

## ✨ Features

- **Zero-Config Architecture:** No need to manually create `.env` files or edit system variables. Everything is handled securely via CLI tokens.
- **Real-Time Telegram Notifications:** Get instant deployment logs (success, failure, build times) directly to your Telegram via secure Magic Tokens.
- **Smart Auto-Rollback:** If a build crashes (e.g., failed `npm build`), Smart Deploy automatically rolls back to the last stable Git commit and restarts your service to prevent downtime.
- **Anti-Sanction Proxy Support:** Built-in proxy routing to seamlessly download dependencies (`npm`, `pip`) on servers with restricted network access.
- **Zero-Touch Webhooks:** Automatically configures GitHub webhooks using your Personal Access Token.
- **Framework Auto-Detection:** Intelligently detects Node.js (Next.js/React) and Python ecosystems.
- **Native Systemd Integration:** Generates Linux background services automatically without requiring manual environment variables.

---

## 📦 Installation

Smart Deploy is published on PyPI. It is highly recommended to use `pipx` to install it globally in an isolated environment on your Linux server:

```bash
# Install using pipx (Recommended for Linux servers)
pipx install smart-deploy

# OR install using standard pip
pip install smart-deploy
```

---

## 🚀 Quick Start

### 1. Link to Telegram Bot (Zero-Config Setup)

Get your Magic Token from our central Telegram bot (`@smartdepbot`) and link your server securely in one step. This eliminates the need for `.env` files:

```bash
smart-deploy bot link eyJ1cmwiOiAiaHR0cDovLz...

```

### 2. Generate & Start the Background Service

To ensure Smart Deploy runs 24/7 and survives server reboots, run the built-in service generator:

```bash
smart-deploy generate-service --port 9000

```

_Follow the on-screen instructions to create, enable, and start the `systemd` service._

### 3. Prepare Your Server Directory

Ensure the target directory on your server is initialized as a Git repository and connected to your GitHub remote:

```bash
cd /var/www/your-project
git init
git remote add origin https://github.com/YourUsername/your-repo.git
git fetch origin
git branch --set-upstream-to=origin/main main

```

### 4. Register Your Project

Link your GitHub repository to the local directory. Smart Deploy will automatically contact the GitHub API and configure the webhook.

**For Standard/Static Projects (e.g., React, Vite):**

```bash
smart-deploy add https://github.com/YourUsername/your-repo \
  /var/www/your-project \
  http://YOUR_SERVER_IP:9000 \
  --token "ghp_your_github_personal_access_token" \
  --restart "npm run build"

```

**For Next.js / Live Node.js Projects (With Proxy & PM2):**

```bash
smart-deploy add https://github.com/YourUsername/your-repo \
  /var/www/your-project \
  http://YOUR_SERVER_IP:9000 \
  --token "ghp_your_github_personal_access_token" \
  --restart "pm2 restart my-app" \
  --proxy "http://127.0.0.1:10808"

```

**Parameters Explained:**

- `Repo URL`: The target GitHub repository URL.
- `Local Path`: The absolute path to your project on the server.
- `Server URL`: Your server's public IP/Domain and the port (e.g., `http://123.45.67.89:9000`).
- `--token`: Your GitHub Personal Access Token (requires `repo` and `admin:repo_hook` permissions).
- `--restart`: (Optional) The command to run after pulling and building the code.
- `--proxy`: (Optional) Local proxy URL to bypass network restrictions during `npm install` or `pip install`.

### 5. Push and Relax

Now, simply push your code from your local machine:

```bash
git commit -m "feat: awesome new feature"
git push

```

Smart Deploy will intercept the webhook, pull the latest code, install dependencies, build the project, restart the service, and send a **beautiful success report to your Telegram**.

---

## 🧠 Smart Detector & Auto-Rollback

When a push webhook is triggered, Smart Deploy analyzes your project:

1. **Pull Code:** Executes `git pull` (routed through your proxy if configured).
2. **Node.js / Next.js**: If `package.json` is found, runs `npm install`. If `next.config.js` is present, proceeds with `npm run build`.
3. **Python**: Locates your virtual environment (`venv`) and runs `pip install -r requirements.txt`.
4. **Execution**: Runs your custom `--restart` command.
5. **🛡️ Auto-Rollback:** If any step fails (e.g., a syntax error crashes the build), Smart Deploy instantly runs `git reset --hard` to the previous commit, restarts your app to keep it online, and alerts you on Telegram.

---

## 🛠️ CLI Commands Reference

- `smart-deploy bot link <TOKEN>`: Securely connect your server to Telegram notifications.
- `smart-deploy add`: Register a project and auto-configure GitHub webhooks.
- `smart-deploy generate-service`: Generate a systemd unit file for Linux.
- `smart-deploy start`: Launch the FastAPI receiver directly in the terminal (for testing).
- `smart-deploy --help`: View the detailed help menu.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

Developed with ❤️ by [Amirtaha Nemati](https://github.com/amirtahanemati).
