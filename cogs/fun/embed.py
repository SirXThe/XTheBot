#  XTheBot
#  Copyright (C) 2022  XThe
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
from disnake import Option, OptionType, ApplicationCommandInteraction
from disnake.ext import commands


class EmbedCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="embed",
        description="Generate a custom embed message.",
        options=[
            Option(
                name="message",
                description="The message of your embed.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="title",
                description="The title of your embed.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="footer",
                description="The footer of your embed.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="color",
                description="The color of your embed.",
                type=OptionType.string,
                required=False,
                choices=["teal", "dark_teal", "green", "dark_green", "blue", "dark_blue", "purple", "dark_purple",
                         "magenta", "dark_magenta", "gold", "dark_gold", "orange", "dark_orange", "red", "dark_red",
                         "lighter_grey", "dark_grey", "light_grey", "darker_grey", "blurple", "greyple"]
            ),
        ],
    )
    async def embed(self, interaction: ApplicationCommandInteraction, message: str, title: str = "",
                    footer: str = "", color: disnake.Colour = 0x8b2d27) -> None:
        embed = disnake.Embed(
            title=title,
            description=message,
            color=color
        )
        embed.set_footer(
            text=footer
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(EmbedCommand(bot))
