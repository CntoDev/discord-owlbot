import discord
from dotenv import dotenv_values
import os

# Load from .env (for local dev environments) or override with environment variables (for production)
config = {
        **dotenv_values('.env'),
        **os.environ
}

CHANNEL_ID = config['OP_START_CHANNEL_ID']

# Read bot token for Discord auth from docker-compose secrets
BOT_SECRET = None
with open('/run/secrets/discord_token', 'r') as f:
        BOT_SECRET = f.read()

if BOT_SECRET is None:
        raise ValueError("Unable to read Discord token")

class MyClient(discord.Client):
     async def on_ready(self):
        # async for guild in client.fetch_guilds(limit=150):
        #         print(guild.name)

        channel = await self.fetch_channel(CHANNEL_ID)
        await channel.send("Tonight's mission will start soon. <@&220093887518081024> and <@&665323023699673108> grab a drink and join us!")
        await self.close()

intents = discord.Intents()
intents.messages = True
intents.guilds = True

client = MyClient(intents=intents)
client.run(BOT_SECRET)
