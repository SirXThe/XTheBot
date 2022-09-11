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

import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class BoredCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="bored",
        description="Show some tips you can do when you are bored.",
    )
    async def bored(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.boredapi.com/api/activity") as request:
                if request.status == 200:
                    json = await request.json(
                        content_type="application/json")
                    embed = disnake.Embed(
                        description=json["activity"],
                        color=0x8b2d27
                    )
                    embed.set_footer(
                        text="Made by XThe"
                    )
                    await interaction.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="The API did not respond, try again later.",
                        color=0x8b2d27
                    )
                    embed.set_footer(
                        text="Made by XThe"
                    )
                    await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(BoredCommand(bot))
