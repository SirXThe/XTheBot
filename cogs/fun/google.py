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

import googlesearch
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class GoogleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="google",
        description="Search something in the world wide web with Google.",
        options=[
            Option(
                name="query",
                description="What do you want to search.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="language",
                description="",
                type=OptionType.string,
                required=True,
                choices=["en", "de", "fr"]
            ),
        ],
    )
    async def google(self, interaction: ApplicationCommandInteraction, query: str, language: str = "en") -> None:
        for result in googlesearch.search(query, num_results=1, lang=language):
            await interaction.send(result)
            break


def setup(bot):
    bot.add_cog(GoogleCommand(bot))
