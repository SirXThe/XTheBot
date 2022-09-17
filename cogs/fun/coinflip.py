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


class CoinflipCommand(commands.Cog):
    def __init__(self, bot):
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


def setup(bot):
    bot.add_cog(CoinflipCommand(bot))
