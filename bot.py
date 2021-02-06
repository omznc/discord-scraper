#! /usr/bin/python3
import discord
import asyncio
import requests
import time 
import json
import os

# A really bad 'settings' page.
parseHubKey = ""  # Parsehub API key
parseHubLink_run = '' # Parsehub run project link
parseHubLink_fetch = '' # Parsehub get latest data link
dataLocation = '' # The json file that stores the last title
botToken = '' # Discord bot token
thumbnailURL = "" # Photo in the embed
sendChannelID = 1337 # Set the channel ID here


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

            # Parsehub stuff
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
                # If there's no content to the post (image-only): 
                if "content" not in data.keys():
                    noPostDescription = "Obavijest nema teksta. Kliknite na naslov da otvorite u browser-u."
                    embed=discord.Embed(title=data["title"], url=data["article_url"], description=noPostDescription, color=0xf6f6f6)
                # If the post contains more text than an embed can support:
                elif len(data["content"])>2000:
                    # If there's a short description:
                    if "short_description" in data.keys():
                        description = f"{data['short_description']} \n\nPoruka preduga. Otvorite u browseru."
                    else:
                        description = "\n\nPoruka preduga. Otvorite u browseru."
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


