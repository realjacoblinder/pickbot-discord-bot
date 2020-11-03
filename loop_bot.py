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
CHANNELS = [int(i) for i in os.getenv('ALL_CHANNELS').split(',')]

client = discord.Client()
async def send_all_channels(message):
    for channel in CHANNELS:
        channel = client.get_channel(channel)
        await channel.send(message)

async def my_background_task():
    await client.wait_until_ready()
    while True:
        await send_all_channels("Autist detector booting up.")
        for comment in reddit.redditor('pickbot').stream.comments(skip_existing=True, pause_after=0):
            if comment is None:
                await asyncio.sleep(1)
                continue
            sub_url = comment.submission.url
            post_flair = str(comment.submission.link_flair_text)
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
            await send_all_channels(f'Flair: {post_flair}\nURL: sub_url\n```\n{pretty_t.get_string()}\n```')
            #await send_all_channels('Flair: {} \n URL: {}'.format(post_flair,sub_url))

@client.event
async def on_ready():
    print('Starting')

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.content.startswith("autists"):
        #print(message.channel.id)
        await message.channel.send("That's us, DINGUS")
    elif message.content.find('liquidate') != -1:
        await message.channel.send('DIAMOND HANDS')

client.loop.create_task(my_background_task())
client.run(TOKEN)
