import discord
from discord.ext import commands
import os
import time
import platform
import datetime
import random

# user classes

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

# views

class RollGameView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Roll", style=discord.ButtonStyle.primary, emoji="🎲" )
    async def roll(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (bot.rollgamectx.in_progress == False):
            print("debug: game already in progress returning...")
            return

        player = interaction.user.name
        print(f"debug: Player {player} tries to roll ...")
        # check if already played

        for registered_player,score in bot.rollgamectx.plays:
            if registered_player == player:
                print(f"debug: Player {player} has already played.")
                await interaction.response.send_message("Juz zagrales matole xD", ephemeral=True)
                return

        rollvalue = random.randint(1, 100)
        print(f"{player} rolled {rollvalue}")
        bot.rollgamectx.plays.append((player, rollvalue))
        print("debug: current plays register: ")
        print(bot.rollgamectx.plays)

        bot.rollgamectx.embed.add_field(name=f":game_die: {interaction.user.name} rolled {rollvalue}", value="", inline=False)
        print("len of rollgame plays: " + str(len(bot.rollgamectx.plays)))

        number_of_plays = len(bot.rollgamectx.plays)
        if (number_of_plays >= 3):
            # finish the game
            best_player = None
            best_score = 0
            for player, score in bot.rollgamectx.plays:
                if score > best_score:
                    best_player = player
                    best_score = score
            bot.rollgamectx.embed.color = color=0xff0000
            bot.rollgamectx.embed.title = f":trophy: WINNER {best_player} (roll {best_score})"
            bot.rollgamectx.embed.add_field(name=f"{best_player} zgrzmotił kompetycje a reszta sie sfrajerzyła tego dnia", value="", inline=True)
            button.disabled = True
            await interaction.response.edit_message(embed=bot.rollgamectx.embed, view=self)
            bot.rollgamectx.reset()
        else:
            # update the game
            await interaction.response.edit_message(embed=bot.rollgamectx.embed)

token = os.getenv('BOT_TOKEN')
if token == None:
    raise Exception('Bot token is invalid!')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.rollgamectx = RollGameContext()
bot.startup_time = datetime.datetime.now()
print(f"marking startup time: {bot.startup_time}")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# slash commands

@bot.tree.command(name="czy", description="Zadaj ważkie pytanie")
async def czy(interaction: discord.Interaction, pytanie: str):
    answers = ["Tak", "Nie", "taknie", "nietak... nie", "Może tak, może nie a może chuj cie wie",
    "Kaseta maszyny losujacej jest pusta... zwolnienie blokady i chuj porozsypywalo sie",
    "Jakbym ja takie rzeczy wiedzial to byloby zajebiscie", "No ta",
    "Na stuweczke", "Lepiej zeby tak bylo", "Swiat takich rzeczy nie widzial", "7 % że nie",
    "9 % że tak", "25 % że nie możliwe że nie", "Możliwe", "Niemożliwe", "Prawdopodobnie huj to strzeli",
    "Gowno byles chuj widziales i w dupie sie znasz", "Gowno znasz chuj byles i w dupie widziales",
    "W dupie sie znasz, gowno widziales i chuj byles", "Taaaakkowoż że nie xD", "NyET cuKa",
    "Nie ma takich rzezy w tym jebanym swiecie", "Tak by wychodzilo", "Tak by wychodzilo ze nie",
    "Aaa stul pysk", "Szansa na to jest niezerowa", "teraz sie tego przewidziec nie da",
    "odpowiedz jest whuj rozmyta, sproboj ponownie", "Pewno", "Napewno"]
    answer = random.choice(answers)
    embed=discord.Embed(title=f"Czy {pytanie}", color=0x6733ff)
    embed.add_field(name="", value=f':crystal_ball: {answer}', inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roll", description="Roll a dice (1-100)")
async def roll(interaction: discord.Interaction):
    value = random.randint(1, 100)
    await interaction.response.send_message(f"{interaction.user.display_name} rolled: **{value}**")

@bot.tree.command(name="uptime", description="Check bot uptime")
async def uptime(interaction: discord.Interaction):
    now = datetime.datetime.now()
    delta = now - bot.startup_time
    await interaction.response.send_message(f"Uptime: **{delta}**.")

@bot.tree.command(name="reset", description="resets the roll game")
async def reset(interaction: discord.Interaction):
    bot.rollgamectx.reset()
    await interaction.response.send_message("Roll game reset.")

@bot.tree.command(name="rollgame", description="starts a roll game")
async def rollgame(interaction: discord.Interaction):
    if (bot.rollgamectx.in_progress == False):
        bot.rollgamectx.in_progress = True
        await interaction.response.send_message("Roll game started.")
        bot.rollgamectx.embed = discord.Embed(title="Roll Game", description="dice game on clayton street", color=0x00ff00, timestamp=datetime.datetime.utcnow())
        bot.rollgamectx.message = await interaction.channel.send(embed=bot.rollgamectx.embed, view=RollGameView())
    else:
        await interaction.response.send_message(f"Zaczekejże {interaction.user.display_name} zjebie, gierka already in progress.")

# prefix commands

@bot.command()
async def sync(ctx: commands.Context, where_to=None):
    if ctx.author.id != 111215610289025024:
        await ctx.send('You must be the owner to use this command!')
        return
    if where_to == "global":
        try:
            bot.tree.copy_global_to(guild=ctx.guild)
            synced = await bot.tree.sync(guild=ctx.guild)
        except:
            print("Failed to sync.")
            return
        print(f"Slash cmds synced: {len(synced)}")
    elif where_to == "guild":
        try:
            bot.tree.copy_global_to(guild=ctx.guild)
            synced = await bot.tree.sync(guild=ctx.guild)
        except:
            print("Failed to sync.")
            return
        print(f"Slash cmds synced: {len(synced)}")
    else:
        await ctx.send('You must specify global or guild sync!')

@bot.command()
async def roll(ctx: commands.Context):
    value = random.randint(1, 100)
    await ctx.send(f"{ctx.author.display_name} rolled: **{value}**")

bot.run(token)
