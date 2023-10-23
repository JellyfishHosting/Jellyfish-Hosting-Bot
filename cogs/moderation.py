import discord
from discord.ext import commands
import config
from datetime import datetime
import datetime
import string
import random
import time
class Moderation(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.slash_command(name="ban", description="Bans the specified user from the guild.", guilds_ids=[config.guild_ids])
    @commands.has_role(1165579899415842877)
    async def ban(self, ctx : commands.Context, member : discord.Option(discord.SlashCommandOptionType.user, description="The user you want to ban", required=True), reason : discord.Option(discord.SlashCommandOptionType.string, description="The reason why you want to ban the user.", required=True)):
        await ctx.defer()
        letters = string.ascii_letters
        stringrandom = ''.join(random.choice(letters) for i in range(6))
        punishment_id = 'JF-' + stringrandom
        logChannel = self.bot.get_channel(config.moderation_log_channel)
        date = datetime.today()
        botuser = self.bot.get_user(self.bot.user.id)
        if member.top_role <= ctx.author.top_role:
            await ctx.followup.send("Sorry, you can not ban someone that has a higher role than you or the same role as you.")
            return
        if botuser.top_role <= member.top_role:
            await ctx.followup.send("Sorry, I can not ban someone that has a higher role than me or the same role as me.")
            return
        embed = discord.Embed(title="User Banned", description="The user has successfully been banned.", color=discord.Color.green())
        embed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        embed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        embed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        memberEmbed = discord.Embed(title="You Have Been Banned!", description="You have been banned from the Jellyfish Hosting guild.\nYou can appeal by emailing: appeals@jellyfishhosting.xyz", color=discord.Color.red())
        memberEmbed.add_field(name="Staff Member: ", value=f"{ctx.author.mention}", inline=False)
        memberEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        memberEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        logEmbed = discord.Embed(title="New Banned User", description=f"A new user has been banned by {ctx.author.mention}", color=discord.Color.blue())
        logEmbed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        logEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        logEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        try:
            await self.bot.punishments.insert({'username': member.name, 'reason': reason, 'staffmember': ctx.author.name, 'timestamp': time.time(), 'punishment_id': punishment_id, 'type': 'ban'})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to add this ban entry to the database.\nError: ```{e}```")
            return
        await member.ban(reason=reason)
        await ctx.followup.send(embed=embed)
        await logChannel.send(embed=logEmbed)
        try:
            await member.send(embed=memberEmbed)
        except Exception as e:
            await ctx.send("The user has not been notified about their ban due to their DMs being closed.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.respond("You are missing the required role to run this command. The role you require is *Ban Perms*.\nIf you believe this is a mistake contact a management member.")

    @commands.slash_command(name="kick", description="Kicks the specified user from the guild.", guilds_ids=[config.guild_ids])
    @commands.has_role(1165579960677826671)
    async def kick(self, ctx : commands.Context, member : discord.Option(discord.SlashCommandOptionType.user, description="The user you want to kick.", required=True), reason : discord.Option(discord.SlashCommandOptionType.string, description="The reason why you want to kick the user.", requiredd=True)):
        await ctx.defer()
        letters = string.ascii_letters
        randomstring = ''.join(random.choice(letters) for i in range(6))
        punishment_id = 'JF-' + randomstring
        logChannel = self.bot.get_channel(config.moderation_log_channel)
        date = datetime.today()
        botuser = self.bot.get_user(self.bot.user.id)
        if member.top_role <= ctx.author.top_role:
            await ctx.followup.send("Sorry, you can not kick someone that has a higher role than you or the same role as you.")
            return
        if botuser.top_role <= member.top_role:
            await ctx.followup.send("Sorry, I can not kick someone that has a higher role than me or the same role as me.")
            return
        embed = discord.Embed(title="User Kicked", description="The user has successfully been kicked.", color=discord.Color.green())
        embed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        embed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        embed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        memberEmbed = discord.Embed(title="You Have Been Kicked!", description="You have been kicked from the Jellyfish Hosting guild. To rejoin go to https://discord.gg/comingsoon", color=discord.Color.red())
        memberEmbed.add_field(name="Staff Member: ", value=f"{ctx.author.mention}", inline=False)
        memberEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        memberEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        logEmbed = discord.Embed(title="New Kicked User", description=f"A new user has been kicked by {ctx.author.mention}", color=discord.Color.blue())
        logEmbed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        logEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        logEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        try:
            await self.bot.punishments.insert({'username': member.name, 'reason': reason, 'staffmember': ctx.author.name, 'timestamp': time.time(), 'punishment_Id': punishment_id, 'type': 'kick'})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to add this kick entry to the database.\nError: ```{e}```")
            return
        await member.kick(reason=reason)
        await ctx.followup.send(embed=embed)
        await logChannel.send(embed=logEmbed)
        try:
            await member.send(embed=memberEmbed)
        except Exception as e:
            await ctx.send("The user has not been notified about their kick due to their DMs being closed.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.respond("You are missing the required role to run this command. The role you require is *Kick Perms*.\nIf you believe this is a mistake contact a management member.")
    
    @commands.slash_command(name="timeout", description="Timesout the specified user from the guild.", guilds_ids=[config.guild_ids])
    @commands.has_role(1165579984312733719)
    async def timeout(self, ctx : commands.Context, member : discord.Option(discord.SlashCommandOptionType.user, description="The user you want to timeout.", required=True), reason : discord.Option(discord.SlashCommandOptionType.string, description="The reason why you want to timeout.", required=True), seconds : discord.Option(int, description="Enter seconds, put 0 if there is none.", required=True), minutes: discord.Option(int, description="Enter minutes, put 0 if there is none.", required=True), hours : discord.Option(int, description="Enter hours, put 0 if there is none.", required=True), days : discord.Option(int, description="Enter days, put 0 if there is none", required=True)):
        await ctx.defer()
        letters = string.ascii_letters
        randomstring = ''.join(random.choice(letters) for i in range(6))
        punishment_id = 'JF-' + randomstring
        logChannel = self.bot.get_channel(config.moderation_log_channel)
        date = datetime.today()
        botuser = self.bot.get_user(self.bot.user.id)
        duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        if member.top_role <= ctx.author.top_role:
            await ctx.followup.send("Sorry, you can not timeout someone that has a higher role than you or the same role as you.")
            return
        if botuser.top_role <= member.top_role:
            await ctx.followup.send("Sorry, I can not timeout someone that has a higher role than me or the same role as me.")
            return
        embed = discord.Embed(title="User Timedout", description="The user has successfully been timedout", color=discord.Color.green())
        embed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        embed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        embed.add_field(Name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        memberEmbed = discord.Embed(title="You Have Been Timedout!", description="You have been timedout from the Jellyfish Hosting guild. You can appeal by emailing appeals@jellyfishhosting.xyz", color=discord.Color.red())
        memberEmbed.add_field(name="Staff Member: ", value=f"{ctx.author.mention}", inline=False)
        memberEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        memberEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        logEmbed = discord.Embed(title="New Timedout User", description=f"A new user has been timedout by {ctx.author.mention}", color=discord.Color.blue())
        logEmbed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        logEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        logEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        try:
            await self.bot.punishments.insert({'username': member.name, 'reason': reason, 'staffmember': ctx.author.name, 'timestamp': time.time(), 'punishment_id': punishment_id, 'type': 'timeout'})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to add this timeout entry to the database.\nError: ```{e}```")
            return
        await member.timeout(duration, reason=reason)
        await ctx.followup.send(embed=embed)
        await logChannel.send(embed=logEmbed)
        try:
            await member.send(embed=memberEmbed)
        except Exception as e:
            await ctx.send("The user has not been notified about their timeout due to their DMs being closed.")

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.respond("You are missing the required role to run this command. The role you require is *Timeout Perms*.\nIf you believe this is a mistake contact a management member.")
    
    @commands.slash_command(name="purge", description="Deletes the specified amount of messages from the channel. (if they are younger than 14 days.)", guild_ids=[config.guild_ids])
    @commands.has_role(1165580024154439731)
    async def purge(self, ctx : commands.Context, amount : discord.Option(int, description="The amount of message you want to delete. (max 100)", required=True)):
        await ctx.defer()
        date = datetime.today()
        logChannel = self.bot.get_channel(config.moderation_log_channel)
        if amount > 100:
            await ctx.followup.send("Sorry, you can only delete up to 100 messages at a time.")
            return
        if amount > 1:
            await ctx.followup.send("You have to want to delete at least 1 message.")
            return
        embed = discord.Embed(title="Messages Purged", description=f"I have successfully deleted {amount} message(s)", color=discord.Color.green())
        logEmbed = discord.Embed(title="New Purge", description=f"A new purge has been requested by {ctx.author.mention}", color=discord.Color.blue())
        logEmbed.add_field(name="Amount: ", value=f"{amount}", inline=False)
        logEmbed.add_field(name="Channel: ", value=f"{ctx.channel.mention}", inline=False)
        logEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        try:
            await ctx.channel.purge(limit=amount)
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to purge the messages.\nError: ```{e}```")
            return
        await ctx.followup.send(embed=embed)
        await logChannel.send(embed=logEmbed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.respond("You are missing the required role to run this command. The role you require is *Purge Perms*.\nIf you believe this is a mistake contact a management member.")

    @commands.slash_command(name="warn", description="Warns the specified user.", guild_ids=[config.guild_ids])
    @commands.has_role(1165580124259881040)
    async def warn(self, ctx : commands.Context, member : discord.Option(discord.SlashCommandOptionType.user, description="The member you want to warn.", required=True), reason : discord.Option(str, description="The reason why you want to warn the member.", required=True)):
        await ctx.defer()
        letters = string.ascii_letters
        randomstring = ''.join(random.choice(letters) for i in range(6))
        punishment_id = 'JF-' + randomstring
        logChannel = self.bot.get_channel(config.moderation_log_channel)
        date = datetime.today()
        botuser = self.bot.get_user(self.bot.user.id)
        if member.top_role >= ctx.author.top_role:
            await ctx.followup.send("You can not warn someone that has a higher role than you or the same role as you.")
            return
        if botuser.top_role >= member.top_role:
            await ctx.followup.send("I can not warn someone that has a higher role than me or the same role as me.")
            return
        embed = discord.Embed(title="User Warned", description="I have successfully warned the user.", color=discord.Color.green())
        embed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        embed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        embed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        memberEmbed = discord.Embed(title="You Have Been Warned!", description="You have been warned in Jellyfish Hosting. To appeal please email appeals@jellyfishhosting.xyz", color=discord.Color.red())
        memberEmbed.add_field(name="Staff Member: ", value=f"{ctx.author.mention}", inline=False)
        memberEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        memberEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        logEmbed = discord.Embed(title="New Warn", description=f"A new user been warned by {ctx.author.mention}", color=discord.Color.blue())
        logEmbed.add_field(name="User Name: ", value=f"{member.mention}", inline=False)
        logEmbed.add_field(name="Reason: ", value=f"{reason}", inline=False)
        logEmbed.add_field(name="Date: ", value=f"{date.day}-{date.month}-{date.year}", inline=False)
        try:
            await self.bot.punishments.insert({"username": member.name, "reason": reason, "timestamp": time.time(), 'punishment_id': punishment_id, 'type': 'warn'})
        except Exception as e:
            await ctx.followup.send("Sorry, there was an error when trying to add the warn entry.\nError: ```{e}```")
            return
        await ctx.followup.send(embed=embed)
        await logChannel.send(embed=logEmbed)
        await member.send(embed=memberEmbed)
def setup(bot):
    bot.add_cog(Moderation(bot))