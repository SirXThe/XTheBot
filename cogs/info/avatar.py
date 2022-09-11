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

import disnake

from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class AvatarCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="avatar",
        description="Get the avatar from a user.",
        options=[
            Option(
                name="user",
                description="The user you want to get the avatar from.",
                type=OptionType.user,
                required=True
            )
        ]
    )
    async def avatar(self, interaction: ApplicationCommandInteraction, user) -> None:
        embed = disnake.Embed(
            title=f"User Avatar from {user}:",
            color=0x8b2d27
        )
        if user.avatar is not None:
            embed.set_image(
                url=user.avatar
            )
        else:
            embed.description = "User does not have an avatar."
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(AvatarCommand(bot))
