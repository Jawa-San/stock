import discord
from discord.ext import commands
import stonk

with open('token.txt', 'r', encoding='utf-8') as f:
    bottoken = f.read()

TOKEN = bottoken
CHANNEL = 1061108864898039818

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
user_watchlist = {}
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL)
    await channel.send("I am ready to display current stock prices!")
    

@bot.command()
async def price(ctx, ticker):
    quote = stonk.get_response(ticker)
    await ctx.send(quote)

@bot.command()
async def watchlist(ctx, op: str, stock = ''):
    user = ctx.message.author.id
    if op == 'add':
        if user in user_watchlist:
            if stock in user_watchlist[user]:
                await ctx.send(f"{stock} is already in your watchlist") 
            else:
                user_watchlist[user][stock] = stonk.get_response(stock)
                await ctx.send(f"adding {stock} to your watchlist")     
        else:
            user_watchlist[user] = {stock: stonk.get_response(stock)}
            await ctx.send(f"adding {stock} to your watchlist")
    if op == 'remove' or op == 'delete':
        if user in user_watchlist:
            if stock in user_watchlist[user]:
                del user_watchlist[user][stock]
                await ctx.send(f"removing {stock} from your watchlist")
            else:
                await ctx.send(f"{stock} not found in your watchlist")
        else:
            await ctx.send("You do not have a watchlist")
    if op == 'show' or op == 'print' or op == 'view':
        if user in user_watchlist:
            message = 'Your watchlist:\n'
            for s, val in user_watchlist[user].items():
                message += f'{s} {val}\n'
            await ctx.send(message)
        else:
            await ctx.send("No stocks in watchlist")
    if op == 'wipe' or op == 'clear':
        if user in user_watchlist:
            user_watchlist[user].clear()
            await ctx.send("Watchlist wiped")
        else:
            await ctx.send("You do not have a watchlist")
        # await ctx.send(f"printing watchlist...")

    

bot.run(TOKEN)
