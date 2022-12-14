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


class NickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        dm_permission=False,
        name="nick",
        description="Nick a user in the server.",
        options=[
            Option(
                name="user",
                description="The user you want to nick.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="name",
                description="The new name for the user.",
                type=OptionType.string,
                required=True
            ),
        ],
    )
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   name: str) -> None:
        user = await interaction.guild.get_or_fetch_member(user.id)
        try:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="**A User got nicked!**",
                description=f"The user **{user}** has been nicked by **{interaction.author}**"
                            f"\n New name: **{name}**"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await user.edit(nick=name)
            await interaction.send(embed=embed)
        except disnake.Forbidden:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not nick the user. Make sure the user isn't Admin or my role is above the user."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(NickCommand(bot))
