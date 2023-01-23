import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import os
import time
import platform

token = os.getenv('BOT_TOKEN')
if token == None:
    raise Exception('Bot token is invalid!')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.command()
async def hello(ctx, member:discord.Member):
    await ctx.send(f"Siema {member.name}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(token)