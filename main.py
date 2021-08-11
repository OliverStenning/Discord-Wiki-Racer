import asyncio
from asyncio.tasks import sleep
import discord
from discord import channel
from discord import message
import requests
from bs4 import BeautifulSoup
import webbrowser
from decouple import config
import wikipedia
from datetime import datetime

client = discord.Client()

startURL = ""
endURL = ""
startTime = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    global startURL
    global endURL
    global startTime

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

        # Generate new random wikipedia page
        endUrlReq = requests.get("https://en.wikipedia.org/wiki/Special:Random")

        # Store URL of new target page
        endURL = endUrlReq.url

        # Get title of page from html
        soup = BeautifulSoup(endUrlReq.content, "html.parser")
        title = soup.find(class_="firstHeading").text

        # Get first paragraph from wikipedia library using title
        description = wikipedia.summary(title, sentences=3)

        await message.channel.send(f"**Target:** {title}\n" \
            f"**Description:** {description}\n\n" \
            "Type /new to select a new Wikipedia page otherwise type /start to reveal the start link.")

    if message.content.startswith('/start'):

        # Generate new random wikipedia page
        startUrlReq = requests.get("https://en.wikipedia.org/wiki/Special:Random")

        # Store URL of new start page
        startURL = startUrlReq.url

        for x in range(3, 0, -1):
            await message.channel.send(x)
            await asyncio.sleep(1)

        await message.channel.send(f"Go!\n{startURL}")
        startTime = datetime.now()


    if message.content.startswith('/finish'):
        if endURL in message.content or "correct" in message.content:
            await message.channel.send(f"{message.author} wins the round!\n")
            endTime = datetime.now()
            difference = endTime - startTime
            seconds = difference.total_seconds()
            minutes = round(seconds / 60)
            seconds = round(seconds % 60)

            await message.channel.send(f"The time taken was {minutes} minutes and {seconds} seconds.\n\nType /new to start a new round.")
        else:
            await message.channel.send("That is the incorrect link!")

client.run(config('TOKEN'))
