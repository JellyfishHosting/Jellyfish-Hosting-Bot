import discord
from discord.ext import commands
import os
import config
import motor.motor_asyncio
from utils.mongo import Document

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), disableEveryone=False)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.users)} users in JFH"))
    print("Bot is ready!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('__'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')
    else:
        continue


if __name__ == "__main__":
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(config.mongo_uri))
    bot.db = bot.mongo['jellyfishhostbot']
    bot.punishments = Document(bot.db, 'punishments')
    bot.economy = Document(bot.db, 'economy')
    bot.suggestions = Document(bot.db, 'suggestions')

bot.run(config.token)