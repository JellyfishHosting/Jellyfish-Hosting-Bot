import discord
from discord.ext import commands
import datetime
import time
import re
import config
swear_words = config.swear_words
blocked_words = []
for word in swear_words:
    blocked_words.append(re.escape(word))
    blocked_words.append(''.join(r'\s*' + re.escape(c) for c in word))

blocked_words_pattern = r'\b(?:' + '|'.join(blocked_words) + r')\b'

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def block_swear_words(text):
        for word in swear_words:
            text = re.sub(word, '****', text, flags=re.IGNORECASE)
        return text


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if re.search(blocked_words_pattern, message.content, re.IGNORECASE):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, please refrain from using inappropiate language.")
        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))