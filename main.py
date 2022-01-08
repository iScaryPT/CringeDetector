import discord
import os
from discord.ext import commands
from CringeDetector import *
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
bot = commands.Bot(command_prefix='#', intents=intents)

#commands
bot.add_cog(CringeDetector(bot))

bot.run(DISCORD_TOKEN)

