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

import disnake
import calendar
from datetime import datetime
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class ServerInfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        dm_permission=False,
        name="serverinfo",
        description="Show some information about the current server."
    )
    async def serverinfo(self, interaction: ApplicationCommandInteraction) -> None:
        date = datetime.strptime(str(interaction.guild.created_at), '%Y-%m-%d %H:%M:%S.%f')
        embed = disnake.Embed(
            color=0x8b2d27,
            title=f"Information about {interaction.guild}",
            description="** >> About**\n"
                        "**ID:**\n"
                        f"{interaction.guild.id}\n"
                        "**Owner**:\n"
                        f"{interaction.guild.owner}\n"
                        "**Created:**\n"
                        f"<t:{calendar.timegm(date.utctimetuple())}:R>\n"
                        "**Members**:\n"
                        f"{interaction.guild.member_count}\n"
                        "**Boosts**:\n"
                        f"Level {interaction.guild.premium_tier} with {interaction.guild.premium_subscription_count} "
                        "boosts.\n\n"
                        "** >> Statistics**\n"
                        "**Channels:**\n"
                        f"{len(interaction.guild.channels)}\n"
                        "**Roles:**\n"
                        f"{len(interaction.guild.roles)}/250\n"
                        "**Emojis:**\n"
                        f"{len(interaction.guild.emojis)}/{interaction.guild.emoji_limit}\n"
                        "**Stickers:**\n"
                        f"{len(interaction.guild.stickers)}/{interaction.guild.sticker_limit}\n\n"
                        "** >> Security**\n"
                        "**Verification Level:**\n"
                        f"{interaction.guild.verification_level}\n"
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerInfoCommand(bot))
