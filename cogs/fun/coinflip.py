import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class CoinflipCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="coinflip",
        description="The bot throws a coin for you.",
        options=[
            Option(
                name="choice",
                description="Enter your choice here.",
                type=OptionType.string,
                required=True,
                choices=["Heads", "Tails"]
            )
        ]
    )
    async def coinflip(self, interaction: ApplicationCommandInteraction, choice: str) -> None:
        bot_choice = random.choice(["Heads", "Tails"])
        if choice == bot_choice:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="You Won!",
                description=f"Your choice was **{choice}** and my choice was **{bot_choice}**."
            )
            embed.set_footer(
                text="Made by XThe"
            )
        else:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="You Lose!",
                description=f"Your choice was {choice} and my choice was {bot_choice}."
            )
            embed.set_footer(
                text="Made by XThe"
            )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(CoinflipCommand(bot))
