import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class RPSCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="rps",
        description="Play a game of rock paper scissors against the bot.",
        options=[
            Option(
                name="choice",
                description="Enter your choice here.",
                type=OptionType.string,
                required=True,
                choices=["Rock", "Paper", "Scissors"]
            )
        ]
    )
    async def rps(self, interaction: ApplicationCommandInteraction, choice: str) -> None:
        bot_choice = random.choice(["Rock", "Paper", "Scissors"])
        if choice == bot_choice:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Draw!",
                description=f"We both choose {choice}. That's a tie!"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed)
        elif choice == "Rock":
            if bot_choice == "Scissors":
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title="You Win!",
                    description=f"Rock smashes scissors! You win!"
                )
                embed.set_footer(
                    text="Made by XThe"
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title="You Lose!",
                    description=f"Paper covers rock! You lose!"
                )
                embed.set_footer(
                    text="Made by XThe"
                )
                await interaction.send(embed=embed)
        elif choice == "Paper":
            if bot_choice == "Rock":
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title="You Win!",
                    description=f"Paper covers rock! You win!"
                )
                embed.set_footer(
                    text="Made by XThe"
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title="You Lose!",
                    description=f"Scissors cuts paper! You lose."
                )
                embed.set_footer(
                    text="Made by XThe"
                )
                await interaction.send(embed=embed)
        elif choice == "Scissors":
            if bot_choice == "Paper":
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title="You Win!",
                    description=f"Scissors cuts paper! You win!"
                )
                embed.set_footer(
                    text="Made by XThe"
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title="You Lose!",
                    description=f"Rock smashes scissors! You lose."
                )
                embed.set_footer(
                    text="Made by XThe"
                )
                await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(RPSCommand(bot))
