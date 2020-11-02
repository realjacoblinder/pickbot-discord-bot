import os
import asyncio
import discord
#from discord.ext import tasks, commands
from dotenv import load_dotenv
import praw
from prettytable import PrettyTable

reddit = praw.Reddit("scraper",user_agent="scraper")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print('Starting')

@client.event
async def on_message(message):
    #print(message.content)
    if message.content.startswith("autists"):
        num = message.content.split()
        if len(num) == 1: num = 5
        elif len(num) == 2: num = int(num[1])
        else:
            await message.channel.send('Usage is autists [number]')
            return
        await message.channel.send("Checking for new picks...")
        async with message.channel.typing():
            the_picks = []
            for comment in reddit.redditor("pickbot").comments.new(limit=num):
                tmp = comment.body.split('\n')[2:-4]
                del tmp[1]
                the_picks.append(tmp)
            pretty_t = PrettyTable()
            tmp = the_picks[0][0].split('|')
            del tmp[0]
            del tmp[-1]
            tmp = [i.strip() for i in tmp]
            tmp = [i.replace('**','') for i in tmp]
            print(tmp)
            pretty_t.field_names = tmp
            for item in the_picks:
                for i in item[1:]:
                    tmp = i.split('|')
                    del tmp[0]
                    tmp = [i.strip() for i in tmp]
                    tmp = [i.replace('**','') for i in tmp]
                    print(tmp)
                    pretty_t.add_row(tmp)
            #await message.channel.send(comment.body.split('\n')[2:-4])
        await message.channel.send(f'```\n{pretty_t.get_string()}\n```')
        print(message.channel.id)

client.run(TOKEN)


