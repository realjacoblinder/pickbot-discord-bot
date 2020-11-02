#! /usr/bin/python3

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
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))

client = discord.Client()

async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL)
    await channel.send('Listener started...')
    while True:
        await channel.send("Autist detector booting up.")
        for comment in reddit.redditor('pickbot').stream.comments(skip_existing=True, pause_after=0):
            if comment is None:
                await asyncio.sleep(1)
                continue
            sub_url = comment.submission.url
            comment = comment.body.split('\n')[2:-4]
            if not comment:
                print("Empty List")
                continue
            del comment[1]
            pretty_t = PrettyTable()
            tmp = comment.pop(0).split('|')
            del tmp[0]
            del tmp[-1]
            tmp = [i.strip() for i in tmp]
            tmp = [i.replace('**','') for i in tmp]
            for index,item in enumerate(tmp):
                if item == "Recorded Stock Price": tmp[index] = "Stock Price"
                if item == "Recorded Premium": tmp[index] = "Premium"
            print(tmp)
            pretty_t.field_names = tmp
            for tmp in comment:
                tmp = tmp.split('|')
                del tmp[0]
                tmp = [k.strip() for k in tmp]
                tmp = [k.replace('**','') for k in tmp]
                print(tmp)
                pretty_t.add_row(tmp)
            await channel.send(f'```\n{pretty_t.get_string()}\n```')
            await channel.send(sub_url)

@client.event
async def on_ready():
    print('Starting')

@client.event
async def on_message(message):
    if message.content.startswith("autists"):
        print(message.channel.id)
        await message.channel.send("That's us, DINGUS")

client.loop.create_task(my_background_task())
client.run(TOKEN)
