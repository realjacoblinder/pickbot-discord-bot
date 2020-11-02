# pickbot-discord-bot
A discord bot that uses praw to grab new positions comments by pickbot from r/wallstreetbets. Credit for pickbot goes to u/pickbot.

## Some notes on the loop structure
praw's stream modules are very robust, but in my testing they did not work well with discord.py's looping background tasks. After some light trial and error (and a lot of fruitless searching), I found that setting the 'pause_after' argument in the stream to 0 and using asyncio.sleep() myself allowed for the loop to function as intended, while still allowing other bot functionality. 
### About the files
I think its clear which file I was using to learn how the loops work. The difference between pickbot.py and loop_bot.py is that the loop runs forever and sends new positions over to the channel, while pickbot waits for a commands and sends the most recent X positions. 
