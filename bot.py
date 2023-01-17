import discord
from discord.ext import commands
import stonk
import matplotlib.pyplot as plt
import numpy as np
import json
import yfinance as yf
import os



with open('token.txt', 'r', encoding='utf-8') as f:
    bottoken = f.read()

TOKEN = bottoken
CHANNEL = 1061108864898039818

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL)
    await channel.send("I am ready to display current stock prices!")
    

@bot.command()
async def price(ctx, ticker):
    quote = stonk.get_response(ticker)
    await ctx.send(quote)


watchlist_file = "watchlist.json"

def load_watchlist():
    try:
        with open(watchlist_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_watchlist(watchlist):
    with open(watchlist_file, "w") as f:
        json.dump(watchlist, f)

@bot.command()
async def addstock(ctx, ticker: str):
    author_id = str(ctx.message.author.id)
    watchlist = load_watchlist()
    ticker = ticker.upper()
    if author_id not in watchlist["users"]:
        watchlist["users"][author_id] = {"watchlist": []}
    if ticker in [s["ticker"] for s in watchlist["users"][author_id]["watchlist"]]:
        await ctx.send(f"{ticker} already exists in your watchlist.")
    else:
        watchlist["users"][author_id]["watchlist"].append({"ticker": ticker})
        save_watchlist(watchlist)
        await ctx.send(f"{ticker} has been added to your watchlist.")

@bot.command()
async def removestock(ctx, ticker: str):
    author_id = str(ctx.message.author.id)
    watchlist = load_watchlist()
    ticker = ticker.upper()
    if author_id not in watchlist["users"]:
        await ctx.send("You don't have any stocks in your watchlist.")
    else:
        if ticker in [s["ticker"] for s in watchlist["users"][author_id]["watchlist"]]:
            watchlist["users"][author_id]["watchlist"] = [s for s in watchlist["users"][author_id]["watchlist"] if s["ticker"] != ticker]
            save_watchlist(watchlist)
            await ctx.send(f"{ticker} has been removed from your watchlist.")
        else:
            await ctx.send(f"{ticker} not found in your watchlist.")

@bot.command()
async def printwatchlist(ctx):
    author_id = str(ctx.message.author.id)
    watchlist = load_watchlist()
    if author_id not in watchlist["users"]:
        await ctx.send("You don't have any stocks in your watchlist.")
    else:
        stocks = [s["ticker"] for s in watchlist["users"][author_id]["watchlist"]]
        await ctx.send(f"Your watchlist: {', '.join(stocks)}")

@bot.command()
async def plotwatchlist(ctx):
    author_id = str(ctx.message.author.id)
    watchlist = load_watchlist()
    user = bot.get_user(ctx.message.author.id)
    if author_id not in watchlist["users"]:
        await ctx.send("You don't have any stocks in your watchlist.")
    else:
        stocks = [s["ticker"] for s in watchlist["users"][author_id]["watchlist"]]
        df = yf.download(stocks[0])
        ax = df.plot(y='Close', label=stocks[0], linewidth=0.85)
        
        for stock in stocks:
            if stock != stocks[0]:
                df = yf.download(stock)
                df.plot(ax=ax, y='Close', label=stock, linewidth=0.85)
        plt.title(f"{user.name}'s Watchlist")
        plt.xlabel('Date')
        plt.ylabel('Close')
        plt.grid(True)
        plt.savefig("images/watchlist.png")
 
        await ctx.send(file=discord.File("images/watchlist.png"))

        os.remove('images/watchlist.png')


bot.run(TOKEN)
