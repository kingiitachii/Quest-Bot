import os, json, random, discord
from discord.ext import commands, tasks
from flask import Flask
import threading
from datetime import datetime

# باش Render ما يطفيش
app = Flask(__name__)
@app.route('/')
def home(): return "Auto Quest Bot Online!"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000))), daemon=True).start()

TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# خزان الكويستات
QUESTS_LIST = [
    "اربح 3 ماتشات رانكد 🏆",
    "اكتب 100 رسالة في الشات 💬",
    "ادخل فويس 1 ساعة 🎤",
    "ساعد 2 اعضاء جدد 🤝",
    "تفاعل ب 20 ايموجي 😂",
    "فوز بدون ما تموت 🔥"
]

QUEST_CHANNEL_FILE = "channel.json"

def get_channel_id():
    if os.path.exists(QUEST_CHANNEL_FILE):
        with open(QUEST_CHANNEL_FILE, 'r') as f:
            return json.load(f).get("channel_id")
    return None

@bot.event
async def on_ready():
    print(f"Auto Quest Online as {bot.user}")
    await bot.tree.sync()
    auto_quest.start()
    print("Auto Quest loop started")

@tasks.loop(hours=24)
async def auto_quest():
    channel_id = get_channel_id()
    if not channel_id: return
    channel = bot.get_channel(channel_id)
    if not channel: return
    
    quest = random.choice(QUESTS_LIST)
    embed = discord.Embed(
        title="🔥 كويست يومي جديد! - Itachi Quest",
        description=f"**المهمة:** {quest}\n\n**الجائزة:** 500 نقطة + رول Akatsuki",
        color=0xff0000,
        timestamp=datetime.now()
    )
    embed.set_footer(text="عندك 24 ساعة باش تكملها!")
    await channel.send("@everyone", embed=embed)

@bot.tree.command(name="set-quest-channel", description="حدد وين يبعث الكويستات الاوتوماتيك")
@app_commands.describe(channel="القناة")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    with open(QUEST_CHANNEL_FILE, 'w') as f:
        json.dump({"channel_id": channel.id}, f)
    await interaction.response.send_message(f"✅ تم! درك الكويستات راح يتبعثو اوتوماتيك في {channel.mention} كل 24 ساعة", ephemeral=True)

@bot.tree.command(name="quest-now", description="طلق كويست درك حالا")
async def quest_now(interaction: discord.Interaction):
    channel_id = get_channel_id()
    if not channel_id:
        return await interaction.response.send_message("❌ دير /set-quest-channel الاول", ephemeral=True)
    
    quest = random.choice(QUESTS_LIST)
    embed = discord.Embed(title="⚡ كويست فوري!", description=f"**{quest}**", color=0xff0000)
    await interaction.response.send_message(f"{interaction.channel.mention}", embed=embed)
    await interaction.channel.send(embed=embed)

@bot.tree.command(name="quests", description="شوف الكويست الحالي")
async def quests(interaction: discord.Interaction):
    quest = random.choice(QUESTS_LIST)
    await interaction.response.send_message(f"📜 **الكويست الحالي:** {quest}")

bot.run(TOKEN)
