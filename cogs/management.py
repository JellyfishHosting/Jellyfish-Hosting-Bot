import discord
from discord.ext import commands
import config
import string
import random

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="announce", description="The command you need to run to send an announcement into the announcement channel.", guild_ids=[config.guild_ids])
    @commands.has_role(1180941257569226873)
    async def announce(self, ctx : commands.Context, title : discord.Option(discord.SlashCommandOptionType.string, description="The title of the announcement", required=True), body : discord.Option(discord.SlashCommandOptionType.string, description="The body of the announcement.", required=True)):
        await ctx.defer()
        announcement_channel_id = config.announcement_channel
        announcement_channel = self.bot.get_channel(announcement_channel_id)
        embed = discord.Embed(title=title, description=body, color=discord.Color.blue())
        embed.set_footer(text=f"Announcement sent by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await announcement_channel.send(embed=embed)
        await announcement_channel.send("<@&1180943086948454491>")
        await ctx.followup.send("Announcement sent!")
    
    @commands.slash_command(name="volstaffannounce", description="The command you need to run to send an announcement to volunteer staff.", guild_ids=[config.guild_ids])
    @commands.has_role(1180943752051830956)
    async def volstaffannounce(self, ctx : commands.Context, title : discord.Option(discord.SlashCommandOptionType.string, description="The title of the announcement.", required=True), body : discord.Option(discord.SlashCommandOptionType.string, description="The body of the announcement.", required=True)):
        await ctx.defer()
        announcement_channel_id = config.volunteer_staff_announcement_channel
        announcement_channel = self.bot.get_channel(announcement_channel_id)
        embed = discord.Embed(title=title, description=body, color=discord.Color.blue())
        embed.set_footer(text=f"Announcement sent by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await announcement_channel.send(embed=embed)
        await announcement_channel.send("<@&1180944424918859838>")
        await ctx.followup.send("Announcement sent!")

    @commands.slash_command(name="suggest", description="Lets you suggest a feature for any of our bots, client panel, or to add a server software.", guild_ids=[config.guild_ids])
    async def suggest(self, ctx : commands.Context, suggestion : discord.Option(discord.SlashCommandOptionType.string, description="Your suggestion", required=True)):
        await ctx.defer()
        suggestion_channel_id = config.suggestion_chanel
        suggestion_channel = self.bot.get_channel(suggestion_channel_id)
        letters = string.ascii_letters
        randomstring = ''.join(random.choice(letters) for i in range(3))
        suggestion_id = 'JFH-' + randomstring
        embed = discord.Embed(title=f"New Suggestion! #{suggestion_id}", description=suggestion, color=discord.Color.blue())
        embed.set_footer(text=f"Suggested by: {ctx.author.name}", icon_url=ctx.author.avatar.url)    
        message = await suggestion_channel.send(embed=embed)
        message_id = message.id
        await self.bot.suggestions.insert({'suggestion_id': suggestion_id, 'message_id': message_id}) 
        await ctx.followup.send("Suggestion posted!")
def setup(bot):
    bot.add_cog(Management(bot))