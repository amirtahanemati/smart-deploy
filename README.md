# 🚀 Smart Deploy

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)
![Typer](https://img.shields.io/badge/Typer-CLI-000000)

**Smart Deploy** is a lightweight, zero-configuration CI/CD tool designed for independent developers and small teams. It bridges the gap between your GitHub repositories and your Linux server, automating the entire deployment process with a single command.

No complex YAML files. No heavy Jenkins pipelines. Just raw efficiency.

## ✨ Features

- **Zero-Config Webhooks**: Automatically configures GitHub webhooks using your Personal Access Token.
- **Smart Framework Detection**: Automatically detects Node.js (Next.js/React) and Python projects.
- **Auto Dependency Resolution**: Runs `npm install`, `npm run build`, or `pip install` based on your project's ecosystem.
- **Custom Post-Deploy Commands**: Seamlessly integrates with process managers like PM2 or Systemd.
- **Multi-Project Support**: Manage dozens of projects on a single server with one lightweight background listener.

---

## 📦 Installation

Since Smart Deploy is built with Python, you can install it directly on your server using `pip`:

```bash
# Clone the repository
git clone [https://github.com/AmirtahaNemati/smart-deploy.git](https://github.com/AmirtahaNemati/smart-deploy.git)
cd smart-deploy

# Install the package globally
pip install -e .
```

---

## 🚀 Quick Start

### 1. Start the Listener

Spin up the background FastAPI server that listens for GitHub push events.

```bash
smart-deploy start --port 9000

```

_(Tip: In a production environment, run this using `nohup` or create a `systemd` service to keep it alive in the background)._

### 2. Register Your Project

Link your GitHub repository to a local directory on your server. Smart Deploy will automatically configure the GitHub webhook for you.

```bash
smart-deploy add [https://github.com/YourUsername/your-repo](https://github.com/YourUsername/your-repo) /var/www/your-project http://YOUR_SERVER_IP:9000 --token "ghp_your_github_token" --restart "pm2 restart my-app"

```

**Parameters Explained:**

- `https://.../your-repo`: The target GitHub repository.
- `/var/www/your-project`: The absolute path to your project on the server.
- `http://YOUR_SERVER_IP:9000`: Your server's public URL/IP and the port the listener is running on.
- `--token`: Your GitHub Personal Access Token (requires `repo` scope to set up webhooks).
- `--restart`: (Optional) The command to run after pulling and building the code.

### 3. Push and Relax

Now, simply push your code from your local machine:

```bash
git commit -m "feat: awesome new feature"
git push origin main

```

Smart Deploy will intercept the webhook, pull the latest code, install dependencies, build the project, and restart the service automatically.

---

## 🧠 How the Smart Detector Works

When a webhook is triggered, Smart Deploy analyzes the target directory:

1. **Next.js / Node.js**: If `package.json` and `next.config.js` are found, it executes `npm install` followed by `npm run build`.
2. **Python**: If `requirements.txt` is found, it automatically locates your virtual environment (`venv`) and runs `pip install -r requirements.txt`.
3. **Custom Execution**: Finally, it runs the custom restart command provided during the `add` step.

---

## 🛠️ CLI Commands Reference

- `smart-deploy add`: Register a new project and set up webhooks.
- `smart-deploy start`: Launch the FastAPI webhook receiver.
- `smart-deploy --help`: View the detailed help menu.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE&utm_source=gemini) file for details.

Developed with ❤️ by [Amirtaha Nemati](https://www.google.com/search?q=https://github.com/AmirtahaNemati&utm_source=gemini).
