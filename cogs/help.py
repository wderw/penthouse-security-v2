import discord
from discord.ext import commands
from discord import app_commands
import random

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.icon = "❓"

    @app_commands.command(name="help", description="Stop it. Get some help.")
    async def send_bot_help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Penthouse-Security manual")
        for cogName in self.bot.cogs:
            cog = self.bot.cogs[cogName]
            for cmd in cog.get_app_commands():
                embed.add_field(
                    name = "",
                    value = f"{cog.icon} /{cmd.name} - {cmd.description}",
                    inline = False
                )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))