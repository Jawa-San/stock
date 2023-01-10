import discord
from discord.ext import commands
import stonk

TOKEN = 'MTA2MTEwNzMwOTIwOTcyMzA0MQ.GNVYix.8Zo_PnpiGs4kkRuJjyXDMrVp7Z9q5dXjqzC4w8'
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


bot.run(TOKEN)
