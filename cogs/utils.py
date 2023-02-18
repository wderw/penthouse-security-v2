import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Utils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: commands.Context, where_to: str):
        if ctx.author.id != 111215610289025024:
            await ctx.send('You must be the owner to use this command!')
            return
        if where_to == "global":
            try:
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            except:
                print("Failed to sync.")
                return
            print(f"Slash cmds synced: {len(synced)}")
        elif where_to == "guild":
            try:
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            except:
                print("Failed to sync.")
                return
            print(f"Slash cmds synced: {len(synced)}")
        else:
            await ctx.send('You must specify global or guild sync!')

    @app_commands.command(name="uptime", description="Check bot uptime")
    async def uptime(self, interaction: discord.Interaction):
        now = datetime.datetime.now()
        delta = now - self.bot.startup_time
        await interaction.response.send_message(f"Uptime: **{delta}**.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utils(bot))
