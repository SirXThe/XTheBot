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

from database import manager as m
import sympy
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        dm_permission=False,
        name="counting_setup",
        description="Setup the counting function.",
        options=[
            Option(
                name="channel_id",
                description="Insert the channel id or leave it blank if you want to use the current channel.",
                type=OptionType.string,
                required=True
            ),
        ],
    )
    async def counting_setup(self, channel_id: int, interaction: ApplicationCommandInteraction):
        m.cursor.execute("SELECT * FROM counting WHERE guild_id = '%s'" % interaction.guild.id)
        test = m.cursor.fetchone()
        if test is None:
            m.new_counting_entry(guild_id=interaction.guild.id,
                                 channel_id=channel_id)
        else:
            guild_id, old_channel_id, count, last_user, fail_message, greedy_message = test
            temp1 = [guild_id, channel_id, count, last_user, fail_message,
                     greedy_message]
            m.cursor.execute(
                "UPDATE counting SET guild_id = ?, channel_id = ?, count = ?, last_user = ?, fail_message = ?, "
                "greedy_message = ? WHERE guild_id = '%s'" %
                temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5]))
            m.connection.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        m.cursor.execute("SELECT * FROM counting WHERE guild_id = '%s'" % message.guild.id)
        temp = m.cursor.fetchone()
        if temp is None:
            return
        else:
            if str(temp[1]) != str(message.channel.id):
                return
            else:
                try:
                    if any(c.isalpha() for c in message.content):
                        return
                    else:
                        current_count = sympy.sympify(message.content)
                except Exception:
                    return
                old_count = int(temp[2])
                if str(message.author.id) == str(temp[3]):
                    reaction = "❌"
                    guild_id, channel_id, old_count, old_last_user, fail_message, greedy_message = temp
                    count = str(0)
                    last_user = str('')
                    temp1 = [guild_id, channel_id, count, last_user, fail_message, greedy_message]
                    m.cursor.execute(
                        "UPDATE counting SET guild_id = ?, channel_id = ?, count = ?, last_user = ?, fail_message = ?, "
                        "greedy_message = ? WHERE guild_id = '%s'" %
                        temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5]))
                    m.connection.commit()
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} was too **greedy!**"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction(reaction)
                    return
                if old_count + 1 != current_count:
                    reaction = "❌"
                    guild_id, channel_id, old_count, old_last_user, fail_message, greedy_message = temp
                    count = str(0)
                    last_user = str('')
                    temp1 = [guild_id, channel_id, count, last_user, fail_message, greedy_message]
                    m.cursor.execute(
                        "UPDATE counting SET guild_id = ?, channel_id = ?, count = ?, last_user = ?, fail_message = ?, "
                        "greedy_message = ? WHERE guild_id = '%s'" %
                        temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5]))
                    m.connection.commit()
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} has **failed** at {old_count + 1}!\n Answer: "
                                    f"{current_count}"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction(reaction)
                    return
                if old_count + 1 == current_count:
                    reaction = "✅"
                    guild_id, channel_id, old_count, old_last_user, fail_message, greedy_message = temp
                    count = str(current_count)
                    last_user = str(message.author.id)
                    temp1 = [guild_id, channel_id, count, last_user, fail_message, greedy_message]

                    m.cursor.execute(
                        "UPDATE counting SET guild_id = ?, channel_id = ?, count = ?, last_user = ?, fail_message = ?, "
                        "greedy_message = ? WHERE guild_id = '%s'" %
                        temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5]))
                    m.connection.commit()
                    if current_count == 3:
                        reaction = "📛"
                    await message.add_reaction(reaction)


def setup(bot):
    bot.add_cog(Counting(bot))
