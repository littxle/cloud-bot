import discord
import os
from dotenv import load_dotenv

import asyncio
import re
import colorama
from discord.commands import Option
from colorama import Fore
import ezcord

from discord import Color
import random


intents = discord.Intents.all()


bot = ezcord.Bot(
    intents=intents,
    debug=[1189922290654269541],
    error_handler=(os.getenv("ERROR_WEBHOOK_URL")),
)




if __name__ == "__main__":
    bot.load_cogs("./cogs/admin")
    bot.load_cogs("./cogs/commands")
    bot.load_cogs("./cogs/bot")
    bot.load_cogs("./cogs/events")
    bot.load_cogs("./cogs/giveway")


    load_dotenv()
    
    bot.run()

