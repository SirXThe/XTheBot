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


class TimeoutCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        dm_permission=False,
        name="timeout",
        description="Timeout a user in the server.",
        options=[
            Option(
                name="user",
                description="The user you want to timeout.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="duration",
                description="The duration (in minutes) how long you want to timeout the user.",
                type=OptionType.integer,
                required=True
            ),
            Option(
                name="reason",
                description="The reason why you want to timeout the user.",
                type=OptionType.string,
                required=False
            ),
        ],
    )
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, interaction: ApplicationCommandInteraction, user: disnake.User, duration: int,
                      reason: str = "No reason provided") -> None:
        user = await interaction.guild.get_or_fetch_member(user.id)
        try:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="**A User got time outed!**",
                description=f"The user **{user}** has been timed out by **{interaction.author}** for **{duration} "
                            f"minutes**!"
                            f"\n Reason: **{reason}**"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed)
            await user.timeout(reason=reason, duration=duration*60)
        except disnake.Forbidden:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could time out the user. Make sure the user isn't Admin or my role is above the user."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(TimeoutCommand(bot))
