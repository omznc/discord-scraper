#! /usr/bin/python3
import discord
from discord.ext import tasks, commands
import asyncio
import requests
import time 
import json
import os

# Settings.
parseHubKey = "parsehub_key_here" 
parseHubLink_run = 'link_here'
parseHubLink_fetch = 'link_here'
botToken = 'bot_token_here'
thumbnailURL = "raw_image_url_here"
sendChannelID = 000

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background.start()
        self.runs = 0

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fit.ba/student"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    @tasks.loop(seconds=120)
    async def background(self):
        self.runs += 1
        print(f"Ran {self.runs} times.")
        params = {"api_key": parseHubKey}
        requests.post(parseHubLink_run, params=params)
        await asyncio.sleep(30)
        r = requests.get(parseHubLink_fetch, params=params)
        data = json.loads(r.text)

        channel = self.get_channel(sendChannelID)
        temp = await channel.history(limit=1).flatten()
        temp = temp[0]
        date = data["date"]

        # Compares the post date to see if it's the same post. I know... not a great solution.
        if date[:-2] not in temp.content:
            if "content" not in data.keys():
                noPostDescription = "Obavijest nema teksta. Kliknite na naslov da otvorite u browser-u."
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=noPostDescription, color=0xf6f6f6)
            elif len(data["content"])>2000:
                if "short_description" in data.keys():
                    description = f"{data['short_description']} \n\nPoruka preduga. Otvorite u browseru."
                else:
                    description = "\n\nPoruka preduga. Otvorite u browseru."
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=description, color=0xf6f6f6)
            else:
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=data["content"], color=0xf6f6f6)

            embed.set_author(name=data["author"])
            embed.set_footer(text="www.omarzunic.com")
            embed.set_thumbnail(url=thumbnailURL)
            
            await channel.send(f"Objavljeno **{date[:-2]}**", embed=embed)
        
    @background.before_loop
    async def before_loop(self):
        print("Waiting until the bot initializes...")
        await self.wait_until_ready()

client = MyClient()
client.run(botToken)


