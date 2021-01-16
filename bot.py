#! /usr/bin/python3
import discord
import asyncio
import requests
import time 
import json
import os

parseHubKey = "" 
parseHubLink_run = ''
parseHubLink_fetch = ''
dataLocation = ''
botToken = ''
thumbnailURL = ""
sendChannelID = 


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.background())

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fit.ba/student"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        
    async def background(self):
        while True:
            params = {"api_key": parseHubKey}
            f = open(dataLocation)
            OldTitle = json.load(f)

            # Bullshit
            requests.post(parseHubLink_run, params=params)
            await asyncio.sleep(30)
            r = requests.get(parseHubLink_fetch, params=params)
            data = json.loads(r.text)

            # Checks if it's the same post. If yes, proceed.
            if OldTitle != data["title"]:
                OldTitle = str(data["title"])
                f = open(dataLocation, "w")
                json.dump(OldTitle, f)
                f.close()
                if "content" not in data.keys():
                    noPostDescription = "Obavijest nema teksta. Kliknite na naslov da otvorite u browser-u."
                    embed=discord.Embed(title=data["title"], url=data["article_url"], description=noPostDescription, color=0xf6f6f6)
                elif len(data["content"])>2000:
                    description = f"{data['short_description']} \n\nPoruka preduga. Otvorite u browseru."
                    embed=discord.Embed(title=data["title"], url=data["article_url"], description=description, color=0xf6f6f6)
                else:
                    embed=discord.Embed(title=data["title"], url=data["article_url"], description=data["content"], color=0xf6f6f6)

                embed.set_author(name=data["author"])
                date = data["date"]
                embed.set_footer(text=date[:-1])
                embed.set_thumbnail(url=thumbnailURL)
                channel = self.get_channel(sendChannelID)
                await channel.send("<@&796116996000579644>", embed=embed)

            await asyncio.sleep(60) # task runs every 30 seconds

client = MyClient()
client.run(botToken)


