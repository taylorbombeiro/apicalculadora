from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import asyncio
from bot import bot, guild_id
from dotenv import load_dotenv
import discord

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN não foi encontrado no .env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(DISCORD_TOKEN))
    yield

app = FastAPI(lifespan=lifespan)

# ✅ Configuração de CORS
origins = [
    "https://calculadora-five-livid.vercel.app",  # Seu frontend na Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Canais permitidos
CALLS_AUTORIZADAS = [
    1344786678568718427, 1344143923404210181, 1344283921956995112,
    1344283993180471296, 1344143923874107508, 1344143923874107509,
    1344143923874107510, 1344284173690736712, 1344284217437196371,
    1344284661060468746, 1344284708191731905, 1352986797742755870,
    1352986870128312390, 1352987307690692750, 1352989895416877166,
    1352989992233992302, 1352990110160916580, 1352990176426590299,
    1344284783345143921, 1344284851670614057, 1344285205694910515,
    1344285250745925652, 1346501758272147508, 1353491047979810917
]

@app.get("/voice-channels")
async def get_voice_channels():
    guild = discord.utils.get(bot.guilds, id=guild_id)
    if not guild:
        return {"error": "Guild não encontrado"}

    channels = [
        {"id": c.id, "name": c.name}
        for c in guild.voice_channels
        if c.id in CALLS_AUTORIZADAS
    ]
    return channels

@app.get("/voice-channel-members")
async def get_channel_members(id: int):
    guild = discord.utils.get(bot.guilds, id=guild_id)
    if not guild:
        return {"error": "Servidor (guild) não encontrado."}

    channel = discord.utils.get(guild.voice_channels, id=id)
    if not channel:
        return {"error": "Canal de voz não encontrado."}

    return [{"id": m.id, "name": m.display_name} for m in channel.members]
