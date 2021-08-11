import discord
from decouple import config

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    # Don't do anything if the message is from the bot
    if message.author == client.user:
        return

    # /hello command
    if message.content.startswith('/hello'):
        await message.channel.send("Hello, I'm WikiRacer Bot! Use /help to see my commands.")

    # /help command
    if message.content.startswith('/help'):
        await message.channel.send("Here is a list of available commands: \n\n" \
            "/new - provides a description of the destination \n" \
            "/start - starts a countdown from 3 and then provides the start link \n" \
            "/finish URL- first person to enter the URL to the destination wins! \n")

    # /new command
    if message.content.startswith('/new'):
        # Do something
        print('new command entered')

    if message.content.startswith('/start'):
        # Do something
        print('start command entered')

    if message.content.startswith('/finish'):
        # Do something
        print('finish commmand entered')

client.run(config('TOKEN'))
