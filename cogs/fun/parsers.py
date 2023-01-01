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

import disnake
from helpers import counting_helpers as parser
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class ParserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        dm_permission=True,
        name="parse"
    )
    async def parse(self, interaction: ApplicationCommandInteraction):
        pass

    @parse.sub_command(
        name="roman",
        description="Parse a roman number.",
        options=[
            Option(
                name="number",
                description="Enter your number you want to parse.",
                type=OptionType.integer,
                required=True
            ),
        ],
    )
    async def roman(self, interaction: ApplicationCommandInteraction, number: int):
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Parsed number:",
            description=parser.Roman(number)
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)

    @parse.sub_command(
        name="binary",
        description="Parse a binary number.",
        options=[
            Option(
                name="number",
                description="Enter your number you want to parse.",
                type=OptionType.integer,
                required=True
            ),
        ],
    )
    async def binary(self, interaction: ApplicationCommandInteraction, number: int):
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Parsed number:",
            description=int(format(number, "b"))
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)

    @parse.sub_command(
        name="alphabet",
        description="Parse a alphabet number.",
        options=[
            Option(
                name="number",
                description="Enter your number you want to parse.",
                type=OptionType.integer,
                required=True
            ),
        ],
    )
    async def alphabet(self, interaction: ApplicationCommandInteraction, number: int):
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Parsed number:",
            description=parser.Letter(number)
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)

def setup(bot):
    bot.add_cog(ParserCommands(bot))
