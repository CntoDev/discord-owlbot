import os
import sys
import discord

# Discord secret and configuration variables retrieval
BOT_SECRET = None
try:
    with open('/run/secrets/discord_token', 'r') as f:
        BOT_SECRET = f.read()
except FileNotFoundError:
    print("No docker secret")
    exit(1)

NOTIFICATION_CHANNEL_ID = os.environ['NOTIFICATION_CHANNEL_ID']
WELCOME_CHANNEL_ID= os.environ['WELCOME_CHANNEL_ID']
GUILD_ID = os.environ['GUILD_ID']
INTERVIEWER_ROLE_ID= os.environ['INTERVIEWER_ROLE_ID']

class OwlbotMemberWelcome(discord.Client):
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


class OwlbotOperationNotification(discord.Client):
    async def on_ready(self):
        channel = await self.fetch_channel(NOTIFICATION_CHANNEL_ID)
        # TODO: remove embedded role ids and overall message to make it configurable
        await channel.send("Tonight's mission will start soon. <@&220093887518081024> and <@&665323023699673108> grab a drink and join us!")
        await self.close()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

if __name__ == '__main__':
    print(BOT_SECRET)
    if len(sys.argv) == 1:
        print("Starting member welcome workflow")
        client = OwlbotMemberWelcome(intents=intents)
    elif len(sys.argv) == 2 and sys.argv[1] == "operation-notification":
        print("Starting operation notification workflow")
        client = OwlbotOperationNotification(intents=intents)
    else:
        print("Invalid parameter. Only 'operation-notification' is allowed.")
        exit(1)
    
    client.run(BOT_SECRET)
