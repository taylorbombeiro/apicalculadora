from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
guild_id = 1344143922611359856  # ou use int(os.getenv("GUILD_ID"))

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

app = FastAPI(lifespan=lifespan)  # ✅ Criado aqui

# ✅ Middleware de CORS vem logo após app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://calculadora-five-livid.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Seus endpoints abaixo
@app.get("/voice-channels")
async def get_voice_channels():
    guild = discord.utils.get(bot.guilds, id=guild_id)
    if not guild:
        return {"error": "Guild não encontrado"}
    return [{"id": c.id, "name": c.name} for c in guild.voice_channels]

@app.get("/voice-channel-members")
async def get_channel_members(id: int):
    guild = discord.utils.get(bot.guilds, id=guild_id)
    if not guild:
        return {"error": "Servidor não encontrado"}
    channel = discord.utils.get(guild.voice_channels, id=id)
    if not channel:
        return {"error": "Canal não encontrado"}
    return [{"id": m.id, "name": m.display_name} for m in channel.members]
