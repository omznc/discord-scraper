import discord
import asyncio
import requests
import time 
import json

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fit.ba/student"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
    async def my_background_task(self):
        params = {"api_key": "My-Scraping-Server-Token"}
        f = open('mydata.json')
        OldTitle = json.load(f)
        print("Read File")
        while True:
            requests.post('My-Scraping-Server', params=params)
            await asyncio.sleep(60)
            r = requests.get('My-Scraping-Server', params=params)
            data = json.loads(r.text)
            # Checks if it's the same response
            if OldTitle != data["title"]:
                OldTitle = str(data["title"])
                f = open("mydata.json", "w")
                json.dump(OldTitle, f)
                f.close()
                print("Wrote to file")
                embed=discord.Embed(title=data["title"], url=data["article_url"], description=data["content"], color=0xf6f6f6)
                embed.set_author(name=data["author"])
                embed.set_footer(text=data["date"])
                channel = self.get_channel(Channel-ID)
                await channel.send(embed=embed)
                await asyncio.sleep(60)
            else:
                await asyncio.sleep(60) # task runs every 60 seconds

client = MyClient()
client.run('BOT-TOKEN')
