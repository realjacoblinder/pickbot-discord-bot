# pickbot-discord-bot
A discord bot that uses praw to grab new positions comments by pickbot from r/wallstreetbets. Credit for pickbot goes to u/pickbot.

## Some notes on the loop structure
praw's stream modules are very robust, but in my testing they did not work well with discord.py's looping background tasks. After some light trial and error (and a lot of fruitless searching), I found that setting the 'pause_after' argument in the stream to 0 and using asyncio.sleep() myself allowed for the loop to function as intended, while still allowing other bot functionality. 
