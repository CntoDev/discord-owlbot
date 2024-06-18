import datetime
import discord
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = os.environ['OP_START_CHANNEL_ID']
BOT_SECRET = os.environ['OWLBOT_SECRET']
GUILD_ID = os.environ['GUILD_ID']
INTERVIEWER_ROLE_ID= os.environ['INTERVIEWER_ROLE_ID']
WELCOME_CHANNEL_ID= os.environ['WELCOME_CHANNEL_ID']
CNTO_TIMEZONE = datetime.timezone(datetime.timedelta(hours=1),"CNTO_TIMEZONE")
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    async def on_ready(self):
        print('Logged on as', self.user)
        guild = await self.fetch_guild(GUILD_ID)

    async def on_member_join(self, member):
        guild = member.guild
        embed = discord.Embed(title="Welcome to CNTO!", color=0xffffff, url="https://cnto-arma.com")
        embed.set_author(name="CNTO Server")
        embed.set_thumbnail(url="https://forum.cnto-arma.com/uploads/default/original/1X/9e032c33053b34a2bd57d7e90ac03250c7fd3054.png")
        embed.add_field(name="", value=f"Hello {member.mention}, Welcome to Carpe Noctem Tactical Operations. Feel free to message an <@&{INTERVIEWER_ROLE_ID}> or take a look at <#{WELCOME_CHANNEL_ID}> if you have any questions! ", inline=True)
        
        # member joined_at function returns datetime object, strf formats output as follows: Day of Week, Number of day, initials of month, year, hour of day in GMT timezone
        embed.set_footer(text=f'{member.joined_at.strftime('%a %d %b %Y, %I:%M%p')}')
        await guild.system_channel.send(embed = embed)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(intents=intents)
client.run(BOT_SECRET)