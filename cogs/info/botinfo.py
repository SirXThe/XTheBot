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

import platform

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class BotInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Show some information about the bot."
    )
    async def botinfo(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Information about the XTheBot.",
            description="**Owners:**\n"
                        "**XThe#4695** and **HugoOV#0979**\n"
                        "**Prefix:**\n"
                        "Slash Commands (/)\n"
                        "**Bot Version:**\n"
                        f"{self.bot.settings['version']}\n"
                        "**Python Version:**\n"
                        f"{platform.python_version()}\n"
                        "**Disnake API Version:**\n"
                        f"{disnake.__version__}\n"
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfoCommand(bot))
