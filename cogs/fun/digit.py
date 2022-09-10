import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class DigitCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="digit",
        description="The bot will generate a random digit.",
        options=[
            Option(
                name="min",
                description="The smallest (possible) value of your generated digit.",
                type=OptionType.integer,
                required=False,
            ),
            Option(
                name="max",
                description="The biggest (possible) value of your generated digit.",
                type=OptionType.integer,
                required=False,
            ),
        ],
    )
    async def digit(self, interaction: ApplicationCommandInteraction, min: int = 1, max: int = 1000) -> None:
        digit = random.randint(min, max)
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Your random number:",
            description=f"{digit}"
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DigitCommand(bot))
