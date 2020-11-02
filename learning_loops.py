import os
import asyncio
import discord
from dotenv import load_dotenv
import praw
from prettytable import PrettyTable

reddit = praw.Reddit("scraper",user_agent="scraper")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

async def pickbot_checker():
    await client.wait_until_ready()
    channel = client.get_channel(771502202907787314)
    count = 0
    while True:
        await channel.send('Testing loops')
        await asyncio.sleep(1)
        await channel.send(count)
        await asyncio.sleep(2)
        count += 1

@client.event
async def on_ready():
    print('Starting')

@client.event
async def on_message(message):
    if message.content.startswith("autists"):
        await message.channel.send("Can do this while looping")

client.loop.create_task(pickbot_checker())
client.run(TOKEN)
