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

from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class RaccoonCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="raccoon",
        description="Show the picture of a raccoon."
    )
    async def raccoon(self, interaction: ApplicationCommandInteraction) -> None:
        url: str = "https://bigraccoon.monster"
        await interaction.send(url)


def setup(bot):
    bot.add_cog(RaccoonCommand(bot))
