import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from flask import Flask
import threading

# ===== باش Render يحسب عندنا بورت =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Itachi Quest is Online!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()
# ======================================

TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

quests_data = {
    "genin": ["اربح 3 ماتشات", "ادخل فويس 30 دقيقة", "تفاعل 50 رسالة"],
    "chunin": ["اربح 10 ماتشات", "ادخل فويس 2 ساعات"],
    "jonin": ["اربح 20 ماتش"]
}

@bot.event
async def on_ready():
    print(f"Itachi Quest is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="quests", description="عرض الكويستات")
async def quests(interaction: discord.Interaction):
    try:
        embed = discord.Embed(title="📜 Itachi Quest - الكاستات", color=0xff0000)
        for rank, qs in quests_data.items():
            embed.add_field(name=rank.upper(), value="\n".join([f"- {q}" for q in qs]), inline=False)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ مقدرتش نجيب الكاست: {e}", ephemeral=True)

@bot.tree.command(name="daily", description="جائزة يومية")
async def daily(interaction: discord.Interaction):
    await interaction.response.send_message(f"✅ {interaction.user.mention} خديت الجائزة اليومية! +100 نقطة")

bot.run(TOKEN)
