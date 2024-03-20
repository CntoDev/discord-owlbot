import discord
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = os.environ['OP_START_CHANNEL_ID']
BOT_SECRET = os.environ['OWLBOT_SECRET']
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
    async def on_member_join(self, member):
        guild = member.guild
        embed = discord.Embed(title="Welcome to CNTO!", color=0xffffff)
        embed.set_author(name="CNTO Server", url="https://cnto-arma.com")
        embed.set_thumbnail(url="https://forum.cnto-arma.com/uploads/default/original/1X/9e032c33053b34a2bd57d7e90ac03250c7fd3054.png")
        embed.add_field(name="", value=f"Hello {member.mention}, Welcome to Carpe Noctem Tactical Operations. Feel free to message an <@&1220127032487313549> or take a look at <#1220122083678490755> if you have any questions! ", inline=True)
        
        # member joined_at function returns datetime object, strf formats output as follows: Day of Week, Number of day, initials of month, year, hour of day in GMT timezone
        embed.set_footer(text=f'{member.joined_at.strftime('%a %d %b %Y, %I:%M%p')}')
        
        await guild.system_channel.send(embed = embed)

    # Test function, allows to test embed used during on_member_join event using jointest in chat.
    # async def on_message (self, message):
    #   channel = self.get_channel(CHANNEL_ID)
    #   guild = message.guild
    #   if message.author == self.user:
    #       return
    #   if message.content == "jointest":
    #       embed = discord.Embed(title="Welcome to CNTO!", color=0xffffff)
    #       embed.set_author(name="CNTO Server", url="https://cnto-arma.com")
    #       embed.set_thumbnail(url="https://forum.cnto-arma.com/uploads/default/original/1X/9e032c33053b34a2bd57d7e90ac03250c7fd3054.png")
    #       embed.add_field(name="", value=f"Hello {message.author.mention}, Welcome to Carpe Noctem Tactical Operations. Feel free to message an <@&1220127032487313549> or take a look at <#1220122083678490755> if you have any questions! ", inline=True)
    #       embed.set_footer(text=f'{message.author.joined_at.strftime('%a %d %b %Y, %I:%M%p')}')
    #       await guild.system_channel.send(embed = embed)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(intents=intents)
client.run(BOT_SECRET)