import sys
import traceback

import discord
from discord.ext import commands

from silicium_bot.configuration import Config
from silicium_bot.database_adapter import DatabaseAdapter
from silicium_bot.globals import G
from .modules import cogs

bot = commands.Bot(command_prefix=";", help_command=None)

# region init

try:
    G.BOT = bot
    G.DB_ADAPTER = DatabaseAdapter()
    G.CFG = Config()
except Exception:
    print("Failed to init")
    print(traceback.format_exc())
    sys.exit(-1)

# endregion init


@bot.event
async def on_ready():
    try:
        for cog in cogs:
            cog.on_ready()
        print(f"Bot ready. Prefix: {bot.command_prefix}")
    except Exception:
        print("Failed to start")
        print(traceback.format_exc())
        sys.exit(-1)


@bot.event
async def on_message(message: discord.Message):
    try:
        if message.author == bot.user:
            return
        for cog in cogs:
            if cog.on_message(message):
                return
        await bot.process_commands(message)
    except Exception:
        print(traceback.format_exc())
