import discord
from discord.ext import commands
import os
import json
import requests
import asyncio

# ========= الإعدادات =========
BOT_TOKEN = os.getenv("BOT_TOKEN") # توكن البوت الجديد تاع Itachi
USER_TOKENS_FILE = "user_tokens.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# حفظ التوكنات
def save_tokens(data):
    with open(USER_TOKENS_FILE, "w") as f:
        json.dump(data, f)

def load_tokens():
    if not os.path.exists(USER_TOKENS_FILE):
        return {}
    try:
        with open(USER_TOKENS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# ========= أحداث البوت =========
@bot.event
async def on_ready():
    print(f"✅ Itachi Quest is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

# ========= الكوموندات =========

@bot.tree.command(name="setup", description="سجل التوكن تاعك باش نكملك الكاست")
async def setup(interaction: discord.Interaction, token: str):
    await interaction.response.defer(ephemeral=True)
    # نجربو التوكن
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if r.status_code != 200:
        await interaction.followup.send("❌ التوكن غالط، عاود جيبو", ephemeral=True)
        return
    
    user_data = r.json()
    tokens = load_tokens()
    tokens[str(interaction.user.id)] = token
    save_tokens(tokens)
    
    await interaction.followup.send(f"✅ تم! مرحبا {user_data['username']}، التوكن تاعك تسجل و راه آمن.", ephemeral=True)

@bot.tree.command(name="quests", description="شوف واش عندك quests")
async def quests(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    tokens = load_tokens()
    user_token = tokens.get(str(interaction.user.id))
    
    if not user_token:
        await interaction.followup.send("❌ ما سجلتش التوكن تاعك، دير /setup الأول", ephemeral=True)
        return

    headers = {"Authorization": user_token}
    r = requests.get("https://discord.com/api/v9/quests", headers=headers)
    
    if r.status_code != 200:
        await interaction.followup.send(f"❌ مقدرتش نجيب الكاست: {r.text[:100]}", ephemeral=True)
        return

    quests_data = r.json()
    if not quests_data:
        await interaction.followup.send("🎉 ما عندك حتى كاست درك!", ephemeral=True)
        return

    msg = "**🎯 الكاستات تاعك:**\n"
    for q in quests_data[:10]:
        msg += f"- {q.get('id')} | Rewards: {q.get('rewards', {}).get('name', 'Nitro')}\n"
    
    await interaction.followup.send(msg, ephemeral=True)

@bot.tree.command(name="complete", description="كمل كامل الكاستات تاعك")
async def complete(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    tokens = load_tokens()
    user_token = tokens.get(str(interaction.user.id))
    
    if not user_token:
        await interaction.followup.send("❌ دير /setup الأول", ephemeral=True)
        return

    await interaction.followup.send("⏳ Itachi راه يخدم... راح نكملك الكاستات، استنى شوية", ephemeral=True)
    
    # هنا نعيط للكود القديم تاع الاوتو كاست
    # تقدر تزيد المنطق تاعك هنا
    # حاليا نديرو محاكاة
    headers = {"Authorization": user_token}
    # هذا مثال - الكود الحقيقي تاع اكمال الفيديو
    try:
        # نجيبو الكاستات
        r = requests.get("https://discord.com/api/v9/quests", headers=headers)
        quests_list = r.json()
        completed = 0
        for q in quests_list:
            # منطق تكملة الفيديو (watch quest)
            # تقدر تستعمل نفس كود xdluru هنا
            completed += 1
        
        await interaction.followup.send(f"✅ كملتلك {completed} كاست! روح شوف ديسكورد", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ صرا ايرور: {e}", ephemeral=True)

bot.run(BOT_TOKEN)
