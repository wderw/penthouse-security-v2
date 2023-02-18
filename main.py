import discord
from discord.ext import commands
import os
import datetime
import asyncio

token = os.getenv('BOT_TOKEN')
if token == None:
    raise Exception('Bot token is invalid!')

class PenthouseSecurity(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
        self.cogslist = ["cogs.utils","cogs.help", "cogs.rollgame", "cogs._8ball"]

    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension(cog)

    async def on_ready(self):
        print(f"We have logged in as {bot.user}")
        bot.startup_time = datetime.datetime.now()
        print(f"marking startup time: {bot.startup_time}")
        channel = self.get_okragly_stul()
        if channel == None:
            print("Error: Can't find okragly_stul")
            return
        print(f"Found okragly_stul's id: {channel.id}")
        await self.papa_timer(channel)

    def get_okragly_stul(self):
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "okragly_stul":
                return channel
        return None

    def get_emoji_id_by_name(self, channel, name):
        emojis = channel.guild.emojis
        for emoji in emojis:
            if emoji.name == name:
                return emoji.id

    async def papa_timer(self, channel):
        papa_emoji_id = self.get_emoji_id_by_name(channel, "jp2")
        while True:
            now = datetime.datetime.now()
            if now.hour == 21 and now.minute == 37:
                await channel.send(f"<:jp2:{papa_emoji_id}>")
                await asyncio.sleep(3600)
            await asyncio.sleep(20)

bot = PenthouseSecurity()
bot.run(token)
