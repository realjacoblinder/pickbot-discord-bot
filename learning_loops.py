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
CHANNELS = [int(i) for i in os.getenv('ALL_CHANNELS').split(',')]

client = discord.Client()

async def send_all_channels(message):
    for channel in CHANNELS:
        channel = client.get_channel(channel)
        await channel.send('Testing')
        await channel.send(message)

async def pickbot_checker():
    await client.wait_until_ready()
    count = 0
    while True:
        await asyncio.sleep(1)
        await send_all_channels(str(count))
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
