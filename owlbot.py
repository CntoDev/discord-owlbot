from discord.ext import tasks
import datetime
import discord
from dotenv import load_dotenv
import os

load_dotenv()

CHANNEL_ID = os.environ['OP_START_CHANNEL_ID']
BOT_SECRET = os.environ['OWLBOT_SECRET']
GUILD_ID = os.environ['GUILD_ID']
CNTO_TIMEZONE = datetime.timezone(datetime.timedelta(hours=1),"CNTO_TIMEZONE")
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        # arg to be accessed with background task to ping users on event start
        self.NEXT_EVENT = datetime.datetime(3000,1,1,0,0,0,0).astimezone(CNTO_TIMEZONE)

    async def on_ready(self):
        print('Logged on as', self.user)
        guild = await self.fetch_guild(GUILD_ID)
        # We access the start time of the first event on the scheduled event list, and we assign the value to the NEXT_EVENT variable
        event_list = await guild.fetch_scheduled_events()
        try:
            self.NEXT_EVENT = event_list[0].start_time.astimezone(CNTO_TIMEZONE)
            print (event_list[0].start_time)
        except IndexError: #create placeholder event if no event is found
            today = datetime.datetime.today().astimezone(CNTO_TIMEZONE)
            expectedNextOp = datetime.datetime.min
            if today.weekday() < 2: #if next op day is Tuesday
                expectedNextOp = today + datetime.timedelta(3-today.weekday())
            elif today.weekday() < 4: # if next op day is friday
                expectedNextOp = today + datetime.timedelta(4-today.weekday())
            elif today.weekday() > 4: # if next op day is tuesday next week
                expectedNextOp = today + datetime.timedelta(8 - today.weekday())

            # set expectedNextOp time to 19:30
            expectedNextOp = datetime.datetime(expectedNextOp.year, expectedNextOp.month, expectedNextOp.day, 19, 30, 0, 0).astimezone(CNTO_TIMEZONE)
            # set expectedNextOp time to 00:00
            expectedNextOpEnd = datetime.datetime(expectedNextOp.year, expectedNextOp.month, expectedNextOp.day, 0, 0, 0, 0).astimezone(CNTO_TIMEZONE) + datetime.timedelta(1)
            expectedNextOpEnd = expectedNextOpEnd + datetime.timedelta(1)
            await guild.create_scheduled_event(name="OP: TBD", start_time=expectedNextOp, end_time=expectedNextOpEnd, entity_type=discord.EntityType.external, privacy_level=discord.PrivacyLevel.guild_only, location="ts.carpenoctem.co")

    async def setup_hook(self) -> None:
        self.event_warning.start() #start warning task

    async def on_member_join(self, member):
        guild = member.guild
        embed = discord.Embed(title="Welcome to CNTO!", color=0xffffff)
        embed.set_author(name="CNTO Server", url="https://cnto-arma.com")
        embed.set_thumbnail(url="https://forum.cnto-arma.com/uploads/default/original/1X/9e032c33053b34a2bd57d7e90ac03250c7fd3054.png")
        embed.add_field(name="", value=f"Hello {member.mention}, Welcome to Carpe Noctem Tactical Operations. Feel free to message an <@&1220127032487313549> or take a look at <#1220122083678490755> if you have any questions! ", inline=True)
        
        # member joined_at function returns datetime object, strf formats output as follows: Day of Week, Number of day, initials of month, year, hour of day in GMT timezone
        embed.set_footer(text=f'{member.joined_at.strftime('%a %d %b %Y, %I:%M%p')}')
        await guild.system_channel.send(embed = embed)
    async def on_scheduled_event_create(self, event):
        if event.start_time == self.NEXT_EVENT: # Not change NEXT_EVENT if the dates match or NEXT_EVENT is further away.
            return
        elif event.start_time < self.NEXT_EVENT: #if new event is earlier than NEXT_EVENT, NEXT_EVENT gets updated.
            self.NEXT_EVENT = event.start_time

    @tasks.loop (seconds=60)
    async def event_warning(self):
        channel= self.get_channel(int(CHANNEL_ID))
        guild = await self.fetch_guild(GUILD_ID)
        now = datetime.datetime.now().astimezone(CNTO_TIMEZONE)
        if self.NEXT_EVENT < now:
            await channel.send("EVENT O'CLOCK")
            self.NEXT_EVENT = datetime.datetime.max.astimezone(CNTO_TIMEZONE)
            print(self.NEXT_EVENT.strftime('%a %d %b %Y, %I:%M%p'))
        
    @event_warning.before_loop
    async def before_event_warning(self):
        await self.wait_until_ready()

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
intents.guild_scheduled_events = True
client = MyClient(intents=intents)
client.run(BOT_SECRET)