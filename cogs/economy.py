import discord
from discord.ext import commands
import config
import random

class Economy(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.slash_command(name="balance", description="Sends the balance of you or the specified user.", guild_ids=[config.guild_ids])
    async def balance(self, ctx : commands.Context, user : discord.Option(discord.SlashCommandOptionType.user, description="The user you would like too look at.", required=False)):
        await ctx.defer()
        if user == None:
            user = ctx.author
        try:
            data = await self.bot.economy.find_by_custom({'username': user.name})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when searching for the user.\nError: ```{e}```")
            return
        if data is None:
            await self.bot.economy.insert({'username': user.name, 'bank': 0, 'wallet': 0})
            data = await self.bot.economy.find_by_custom({'username': user.name})
        bank_balance = data.get('bank')
        wallet_balance = data.get('wallet')
        embed = discord.Embed(title="Balance", description=f"Here is the balance of {user.mention}.", color=discord.Color.blue())
        embed.add_field(name="Bank Balance: ", value=f"{bank_balance}", inline=False)
        embed.add_field(name="Wallet Balance: ", value=f"{wallet_balance}", inline=False)
        await ctx.followup.send(embed=embed)

    @commands.slash_command(name="beg", description="Begs random people for money.", guild_ids=[config.guild_ids])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx : commands.Context):
        await ctx.defer()
        begamount = random.randint(1, 100)
        try:
            data = await self.bot.economy.find_by_custom({'username': ctx.author.name})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when searching for the user.\nError: ```{e}```")
            return
        if data is None:
            await ctx.followup.send("Sorry, you don't have a economy account. Please do /balance to create one.")
            return
        wallet_balance = data.get('wallet')
        await self.bot.economy.update_by_custom({'username': ctx.author.name}, {'wallet': wallet_balance+begamount})
        await ctx.followup.send(f"You did some begging on the streets. Some kind person gave you {begamount} coin(s).")

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"Slow it down! You can only beg every 60 seconds. Try again in {error.retry_after:.2f}s!")
            
    @commands.slash_command(name="rob", description="Robs the specified person for a random amount of money that they have in their wallet.", guild_ids=[config.guild_ids])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def rob(self, ctx : commands.Context, user : discord.Option(discord.SlashCommandOptionType.user, description="The user you want to rob", required=True)):
        await ctx.defer()
        try:
            victimData = await self.bot.economy.find_by_custom({'username': user.name})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when searching for the user.\nError: ```{e}```")
            return
        if victimData is None:
            await ctx.followup.send("This user doesn't have an economy account!")
            return
        try:
            robberData = await self.bot.economy.find_by_custom({'username': ctx.author.name})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when searching for the robber.\nError: ```{e}```")
            return
        if robberData is None:
            await ctx.followup.send("You don't have an economy account. Please create one by doing /balance!")
            return
        victim_wallet_balance = victimData.get('wallet')
        robber_wallet_balance = robberData.get('wallet')
        if victim_wallet_balance < 100:
            await ctx.followup.send("Its not worth robbing this person!")
            return
        robbed_ammount = random.randint(0, victim_wallet_balance)
        try:
            await self.bot.economy.update_by_custom({'username': ctx.author.name}, {'wallet': robber_wallet_balance+robbed_ammount})
            await self.bot.economy.update_by_custom({'username': user.name}, {'wallet': victim_wallet_balance-robbed_ammount})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when updating the database document.\nError: ```{e}```")
            return
        await ctx.followup.send(f"Robbery successfull! You successfully robbed {user.name} for the amount of {robbed_ammount} coins")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"Slow it down! You can only rob someone every 1 hour. Try again in {error.retry_after:.2f}s!")

    @commands.slash_command(name="deposit", description="Deposits money into your bank account.", guild_ids=[config.guild_ids])
    async def deposit(self, ctx : commands.Context, amount : discord.Option(discord.SlashCommandOptionType.integer, description="The amount of money you want to deposit.", required=True)):
        await ctx.defer()
        if amount < 1:
            await ctx.followup.send("You have to deposit at least 1 coin.")
            return
        try:
            data = await self.bot.economy.find_one({'username': ctx.author.name})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to find the bank data.\nError: ```{e}```")
            return
        if data is None:
            await ctx.followup.send("You don't have an economy account. Please create one by doing /balance.")
            return
        wallet_amount = data.get('wallet')
        bank_amount = data.get('bank')
        if wallet_amount < amount:
            await ctx.followup.send(f"Sorry, you do not have {amount} coins in your wallet.")
            return
        updated_bank_amount = bank_amount + amount
        updated_wallet_amount = wallet_amount - amount
        try:
            await self.bot.economy.update_by_custom({'username': ctx.author.name}, {'bank': updated_bank_amount, 'wallet': updated_wallet_amount})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to add the updated amount.\nError: ```{e}```")
            return
        await ctx.followup.send(f"Success! I have deposited {amount} coins into your bank account.")

    @commands.slash_command(name="withdraw", description="Withdraws money from your bank account.", guild_ids=[config.guild_ids])
    async def withdraw(self, ctx : commands.Context, amount : discord.Option(discord.SlashCommandOptionType.integer, description="The amount of money you want to withdraw.", required=True)):
        await ctx.defer()
        if amount < 1:
            await ctx.followup.send("You have to deposit at least 1 coin.")
            return
        try:
            data = await self.bot.economy.find_one({'username': ctx.author.name})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to find the bank data.\nError: ```{e}```")
            return
        if data is None:
            await ctx.followup.send("You don't have an economy account. Please create one by doing /balance!")
            return
        wallet_amount = data.get('wallet')
        bank_amount = data.get('bank')
        if bank_amount < amount:
            await ctx.followup.send(f"Sorry, you do not have {amount} coins in your wallet.")
            return
        updated_wallet_amount = wallet_amount + amount
        update_bank_amount = bank_amount - amount
        try:
            await self.bot.economy.update_by_custom({'username': ctx.author.name}, {'bank': update_bank_amount, 'wallet': updated_wallet_amount})
        except Exception as e:
            await ctx.followup.send(f"Sorry, there was an error when trying to add the updated amount.\nError: ```{e}```")
            return
        await ctx.followup.send(f"Success! You have withdrawn {amount} coins from your bank account.")
    
    

def setup(bot):
    bot.add_cog(Economy(bot))