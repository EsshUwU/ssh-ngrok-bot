import os
import subprocess
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
username = os.getenv("username")
discord_id = int(os.getenv("discord_id"))

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

ngrok_process = None  # Global handle

def start_ngrok():
    global ngrok_process

    # Kill any running ngrok processes
    subprocess.run(["killall", "-q", "ngrok"])
    time.sleep(1)

    # Start ngrok on port 22
    ngrok_process = subprocess.Popen(["ngrok", "tcp", "22"], stdout=subprocess.DEVNULL)
    time.sleep(5)

    try:
        tunnel_data = requests.get("http://localhost:4040/api/tunnels").json()
        for tunnel in tunnel_data["tunnels"]:
            if tunnel["proto"] == "tcp":
                public_url = tunnel["public_url"]
                host_port = public_url.replace("tcp://", "").split(":")
                return f"ssh {username}@{host_port[0]} -p {host_port[1]}"
        return "No ngrok TCP tunnel found."
    except Exception as e:
        return f"Failed to get ngrok tunnel: {e}"


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        ssh_link = start_ngrok()
        await channel.send("===== ✅ Ngrok Tunnel ready=====")
        await channel.send(f"{ssh_link}")
        await channel.send(f"===== ✅ Ngrok Tunnel ready <@{discord_id}> =====")
        print("Ngrok tunnel started and ready to use.")

@bot.command()
async def restart(ctx):
    if str(ctx.channel.id) == str(CHANNEL_ID):
        ssh_link = start_ngrok()
        await ctx.send("===== 🔁 Ngrok Tunnel Restarted=====")
        await ctx.send(f"{ssh_link}")
        await ctx.send("===== 🔁 Ngrok Tunnel Restarted=====")

    else:
        await ctx.send("❌ You can't use that here.")

@bot.command()
async def stop(ctx):
    if str(ctx.channel.id) == str(CHANNEL_ID):
        subprocess.run(["killall", "-q", "ngrok"])
        await ctx.send("===== 🛑 Ngrok tunnel stopped =====")
        await ctx.send("🛑 Ngrok tunnel stopped.")
        await ctx.send("===== 🛑 Ngrok tunnel stopped =====")

    else:
        await ctx.send("❌ You can't use that here.")

@bot.command()
async def start(ctx):
    if str(ctx.channel.id) == str(CHANNEL_ID):
        subprocess.run(["killall", "-q", "ngrok"])
        ssh_link = start_ngrok()
        await ctx.send("===== ▶️ Ngrok Tunnel Started =====")
        await ctx.send(f"{ssh_link}")
        await ctx.send("===== ▶️ Ngrok Tunnel Started =====")

    else:
        await ctx.send("❌ You can't use that here.")

@bot.command()
async def quit(ctx):
    if str(ctx.channel.id) == str(CHANNEL_ID):
        await ctx.send("👋 Shutting down bot.")
        await bot.close()
    else:
        await ctx.send("❌ You can't use that here.")

@bot.command()
async def ssh_restart(ctx):
    if str(ctx.channel.id) == str(CHANNEL_ID):
        await ctx.send("🔄 Restarting SSH service...")
        subprocess.run(["sudo", "systemctl", "restart", "ssh"])
        time.sleep(3)  # Allow SSH to restart fully

        await ctx.send("🔁 Restarting ngrok tunnel...")

        ssh_link = start_ngrok()
        await ctx.send("===== 🔁 SSH & Ngrok Restarted =====")
        await ctx.send(f"{ssh_link}")
        await ctx.send("===== 🔁 SSH & Ngrok Restarted =====")

    else:
        await ctx.send("❌ You can't use that here.")




bot.run(DISCORD_TOKEN)


