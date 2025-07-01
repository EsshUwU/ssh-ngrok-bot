# Ngrok SSH Bot for Discord

This Python bot runs on a Linux server and exposes SSH access via an Ngrok TCP tunnel. It sends the SSH connection details to a specified Discord channel and lets you manage the tunnel remotely through commands.

---

## 🚀 Features

- 🔐 Automatically starts Ngrok on port 22 (SSH)
- 📩 Sends SSH command to your Discord server/channel
- 🔁 Remote commands:
    - `!start` – Start Ngrok
    - `!stop` – Stop Ngrok
    - `!restart` – Restart Ngrok
    - `!ssh_restart` – Restart SSH + Ngrok
    - `!quit` – Shut down the bot

---

## ⚙️ Requirements

- Python 3.8+
- A [Ngrok](https://ngrok.com) account with authtoken set
- A Discord bot + token
- A Linux system with SSH server (`openssh-server`) installed

---

## 📦 Installation

```bash
# Clone the repo or copy the script to your folder
cd ~/my-bot-folder

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### `requirements.txt`

```
discord.py
python-dotenv
requests
```

---

## 🛠️ .env Configuration

Create a `.env` file in your project directory:

```
DISCORD_TOKEN=your_discord_bot_token
CHANNEL_ID=your_channel_id_as_integer
username=your_linux_username
discord_id=your_discord_id
```

---

## 🛠️ Auto Start on Boot (Linux)

### 1. Create a systemd service

```bash
sudo nano /etc/systemd/system/sshbot.service
```

Paste the following (adjust paths and username):

```ini
[Unit]
Description=Discord SSH Ngrok Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/home/your_username/your-bot-folder
ExecStart=/home/your_username/your-bot-folder/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Enable and start the service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable sshbot.service
sudo systemctl start sshbot.service
```

### 3. View bot logs

```bash
journalctl -u sshbot.service -f
```

---

## 🔑 SSH Key Authentication (Recommended)

On your client machine, generate an SSH key:

```bash
ssh-keygen
```

Connect to the Ngrok tunnel and upload the key:

```bash
ssh-copy-id -p PORT your_username@ngrok-host
```

(Optional) Disable password login for SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Set:

```
PasswordAuthentication no
```

Then restart SSH:

```bash
sudo systemctl restart ssh
```

---

## 💬 Available Discord Commands

- `!start` — Start Ngrok tunnel
- `!stop` — Stop Ngrok tunnel
- `!restart` — Restart Ngrok tunnel
- `!ssh_restart` — Restart SSH service & Ngrok tunnel
- `!quit` — Shut down the bot

---

## ⚠️ Notes

- Use with caution — exposing SSH over Ngrok can be risky if not properly secured
- Prefer SSH key-based authentication
- Rotate Ngrok tunnels frequently to avoid reuse or exposure
- Consider IP restrictions or 2FA on your system if possible