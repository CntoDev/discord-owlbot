import discord
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = os.enivon['OP_START_CHANNEL_ID']
BOT_SECRET = os.environ['OWLBOT_SECRET']

class MyClient(discord.Client):
     async def on_ready(self):
        # async for guild in client.fetch_guilds(limit=150):
        #         print(guild.name)

        channel = self.get_channel(CHANNEL_ID)
        await channel.send("Tonight's OP is about to start, @here grab a drink and join us!")
        await self.close()

intents = discord.Intents()
intents.messages = True
intents.guilds = True

client = MyClient(intents=intents)
client.run(BOT_SECRET)
