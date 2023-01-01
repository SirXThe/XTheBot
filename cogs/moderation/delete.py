#  XTheBot - A multifunctional bot for Discord.
#  Copyright (C) 2022 - 2023 XThe
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
from disnake import ApplicationCommandInteraction, OptionType, Option
from disnake.ext import commands


class DeleteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        dm_permission=False,
        name="delete",
        description="Delete a number of messages.",
        options=[
            Option(
                name="amount",
                description="The number of messages you want to delete.",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def delete(self, interaction: ApplicationCommandInteraction, amount: int) -> None:
        try:
            clear = await interaction.channel.purge(limit=amount)
            if len(clear) == 1:
                embed = disnake.Embed(
                    title="Message was deleted!",
                    description=f"1 message was successfully deleted by {interaction.author}!",
                    color=0x8b2d27
                )
                embed.set_footer(
                    text="Made by XThe"
                )
            else:
                embed = disnake.Embed(
                    title="Messages were deleted!",
                    description=f"{len(clear)} messages were successfully deleted by {interaction.author}!",
                    color=0x8b2d27
                )
                embed.set_footer(
                    text="Made by XThe"
                )
            await interaction.send(embed=embed)
        except Exception:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not delete all messages successfully. Maybe your amount was too big."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(DeleteCommand(bot))
