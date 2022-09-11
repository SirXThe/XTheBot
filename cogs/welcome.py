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
from disnake.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        channel = member.guild.system_channel
        if channel is not None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Member Joined!",
                description=f"**{member}** joined the server. There are now **{channel.guild.member_count}**"
                            f" members."
            )
            try:
                await channel.send(embed=embed)
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title=f"Thanks for joining {channel.guild}!"
                )
                await member.send(embed=embed)
            except:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        channel = member.guild.system_channel
        if channel is not None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Member Left!",
                description=f"**{member}** left the server. There are now **{channel.guild.member_count}**"
                            f" members."
            )
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
