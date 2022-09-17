"""
XTheBot
Copyright (C) 2022  XThe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class DigitCommand(commands.Cog):
    def __init__(self, bot):
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


def setup(bot):
    bot.add_cog(DigitCommand(bot))
