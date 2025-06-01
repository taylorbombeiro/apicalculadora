# main.py (sua API FastAPI com o bot)
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(bot.start(DISCORD_TOKEN))
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/voice-channels")
async def get_voice_channels():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if not guild:
        return {"error": "Guild não encontrado"}
    return [{"id": c.id, "name": c.name} for c in guild.voice_channels]

@app.get("/voice-channel-members")
async def get_channel_members(id: int):
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if not guild:
        return {"error": "Guild não encontrado"}
    channel = discord.utils.get(guild.voice_channels, id=id)
    if not channel:
        return {"error": "Canal de voz não encontrado"}
    return [{"id": m.id, "name": m.display_name} for m in channel.members]

@app.get("/debug")
async def debug():
    return {
        "guilds": [g.name for g in bot.guilds],
        "guild_ids": [g.id for g in bot.guilds]
    }
