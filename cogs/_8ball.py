import discord
from discord.ext import commands
from discord import app_commands
import random

class _8Ball(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="czy", description="Zadaj ważkie pytanie")
    async def czy(self, interaction: discord.Interaction, pytanie: str):
        answers = ["Tak", "Nie", "taknie", "nietak... nie", "Może tak, może nie a może chuj cie wie",
        "Kaseta maszyny losujacej jest pusta... zwolnienie blokady i chuj porozsypywalo sie",
        "Jakbym ja takie rzeczy wiedzial to byloby zajebiscie", "No ta",
        "Na stuweczke", "Lepiej zeby tak bylo", "Swiat takich rzeczy nie widzial", "7 % że nie",
        "9 % że tak", "25 % że niemożliwe że nie", "Możliwe", "Niemożliwe", "Prawdopodobnie huj to strzeli",
        "Gowno byles chuj widziales i w dupie sie znasz", "Gowno znasz chuj byles i w dupie widziales",
        "W dupie sie znasz, gowno widziales i chuj byles", "Taaaakkowoż że nie xD", "NyET cuKa",
        "Nie ma takich rzezy w tym jebanym swiecie", "Tak by wychodzilo", "Tak by wychodzilo ze nie",
        "Aaa stul pysk", "Szansa na to jest niezerowa", "teraz sie tego przewidziec nie da",
        "odpowiedz jest whuj rozmyta, sproboj ponownie", "Pewno", "Napewno",
        "Konsultuje z ChatGPT... Mowi ze predzej sie planety w huja uloza",
        "Konsultuje z ChatGPT...    Ta... No ta... ok dzieki. Mowi ze pytanie idiotyczne",
        "Zgoogluj se cwaniaczku", "Sluchaj no kolego takie pytania to wiesz... no",
        "wiem ale nie powiem hehe", "gźdiba dumbidibaj apszz",
        "tymbarka se otworz i moze ci zakretka odpowie bo ja na pewno nie. zjebie."]
        answer = random.choice(answers)
        embed=discord.Embed(title=f"Czy {pytanie}", color=0x6733ff)
        embed.add_field(name="", value=f':crystal_ball: {answer}', inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(_8Ball(bot))