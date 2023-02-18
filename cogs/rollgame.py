import discord
from discord.ext import commands
from discord import app_commands
import datetime
import random

class Rollgame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.icon = "🎲"
        self.rollgamectx = RollGameContext()
    
    @app_commands.command(name="reset", description="resets the roll game")
    async def reset(self, interaction: discord.Interaction):
        self.rollgamectx.reset()
        await interaction.response.send_message("Roll game reset.")

    @app_commands.command(name="rollgame", description="starts a roll game")
    async def rollgame(self, interaction: discord.Interaction):
        if (self.rollgamectx.in_progress == False):
            self.rollgamectx.in_progress = True
            await interaction.response.send_message("Roll game started.")
            self.rollgamectx.embed = discord.Embed(title="Roll Game", description="dice game on clayton street", color=0x00ff00, timestamp=datetime.datetime.utcnow())
            self.rollgamectx.message = await interaction.channel.send(embed=self.rollgamectx.embed, view=RollGameView(self.rollgamectx))
        else:
            await interaction.response.send_message(f"Zaczekejże {interaction.user.display_name} zjebie, gierka already in progress.")

    @app_commands.command(name="roll", description="Roll dice (1-100)")
    async def roll(self, interaction: discord.Interaction):
        value = random.randint(1, 100)
        await interaction.response.send_message(f"{interaction.user.display_name} rolled: **{value}**")        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Rollgame(bot))

class RollGameContext:
    def __init__(self):
        self.in_progress: bool
        self.message: discord.Message
        self.embed: discord.Embed
        self.plays: list
        self.reset()
    def reset(self):
        self.in_progress = False
        self.message = None
        self.embed = None
        self.plays = []

class RollGameView(discord.ui.View):
    def __init__(self, rollgamectx):
        super().__init__(timeout=None)
        self.rollgamectx = rollgamectx

    @discord.ui.button(label="Roll", style=discord.ButtonStyle.primary, emoji="🎲" )
    async def roll(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (self.rollgamectx.in_progress == False):
            print("debug: game already in progress returning...")
            return

        player = interaction.user.name
        print(f"debug: Player {player} tries to roll ...")
        # check if already played

        for registered_player,score in self.rollgamectx.plays:
            if registered_player == player:
                print(f"debug: Player {player} has already played.")
                await interaction.response.send_message("Juz zagrales matole xD", ephemeral=True)
                return

        rollvalue = random.randint(1, 100)
        print(f"{player} rolled {rollvalue}")
        self.rollgamectx.plays.append((player, rollvalue))
        print("debug: current plays register: ")
        print(self.rollgamectx.plays)

        self.rollgamectx.embed.add_field(name=f":game_die: {interaction.user.name} rolled {rollvalue}", value="", inline=False)
        print("len of rollgame plays: " + str(len(self.rollgamectx.plays)))

        number_of_plays = len(self.rollgamectx.plays)
        if (number_of_plays >= 3):
            # finish the game
            best_player = None
            best_score = 0
            for player, score in self.rollgamectx.plays:
                if score > best_score:
                    best_player = player
                    best_score = score
            self.rollgamectx.embed.color = color=0xff0000
            self.rollgamectx.embed.title = f":trophy: WINNER {best_player} (roll {best_score})"
            self.rollgamectx.embed.add_field(name=f"{best_player} zgrzmotił kompetycje a reszta sie sfrajerzyła tego dnia", value="", inline=True)
            button.disabled = True
            await interaction.response.edit_message(embed=self.rollgamectx.embed, view=self)
            self.rollgamectx.reset()
        else:
            # update the game
            await interaction.response.edit_message(embed=self.rollgamectx.embed)


