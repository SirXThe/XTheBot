#  XTheBot - A multifunctional bot for Discord.
#  Copyright (C) 2022 - 2023  XThe
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class SentenceCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="sentence",
        description="The bot will randomise your sentence.",
        options=[
            Option(
                name="sentence",
                description="The sentence you want to randomise.",
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def sentence(self, interaction: ApplicationCommandInteraction, sentence: str) -> None:
        str_var = list(sentence)
        random.shuffle(str_var)
        embed = disnake.Embed(
            title=f"The randomised sentence:",
            description=f"{''.join(str_var)}",
            color=0x8b2d27
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(SentenceCommand(bot))
