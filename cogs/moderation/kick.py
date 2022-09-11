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
from disnake import Option, OptionType, ApplicationCommandInteraction
from disnake.ext import commands


class KickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        dm_permission=False,
        name="kick",
        description="Kick a user from the server.",
        options=[
            Option(
                name="user",
                description="The user you want to kick.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason why you want to kick the user.",
                type=OptionType.string,
                required=False
            ),
        ],
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   reason: str = "No reason provided") -> None:
        user = await interaction.guild.get_or_fetch_member(user.id)
        try:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="**A User got kicked!**",
                description=f"The user **{user}** has been kicked by **{interaction.author}**."
                            f"\n Reason: **{reason}**"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await user.kick(reason=reason)
            await interaction.send(embed=embed)

        except disnake.Forbidden:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not kick the user. Make sure the user isn't owner and my role is above the user."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(KickCommand(bot))
