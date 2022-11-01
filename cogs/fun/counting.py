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
import calendar
import logging
import random
from datetime import datetime

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, ChannelType
from disnake.ext import commands

from database import manager as db
from helpers import helpers


class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        dm_permission=False,
        name="counting"
    )
    async def counting(self, interaction: ApplicationCommandInteraction):
        pass

    @counting.sub_command(
        name="setup",
        description="Setup the counting function.",
        options=[
            Option(
                name="channel",
                description="Select your counting channel (Text Channel only!).",
                type=OptionType.channel,
                required=True
            ),
        ],
    )
    async def counting_setup(self, interaction: ApplicationCommandInteraction, channel: disnake.TextChannel):
        if not channel.type == ChannelType.text or not ChannelType.news:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description=f"Please select a text channel!"
            )
            await interaction.send(embed=embed, ephemeral=True)
            return
        c = await db.counting_check_entry(interaction.guild.id)
        if c is None:
            await db.counting_new_entry(interaction.guild.id, channel.id, "Normal")
        else:
            await db.counting_update_entry(interaction.guild.id, channel.id, "Normal", c[3],
                                           c[4], c[5], c[6], c[7], c[8], c[9])
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Updated Channel!",
            description=f"Updated channel to {channel.mention}!\n"
                        f"The counting mode is now set to **{c[2]}**."
        )
        await interaction.send(embed=embed)
        if not interaction.channel.id == channel.id:
            await channel.send(embed=embed)

    @counting.sub_command(
        name="server",
        description="Show the statistics for the current server."
    )
    async def server(self, interaction: ApplicationCommandInteraction):
        i = await db.counting_check_entry(interaction.guild.id)
        date = (datetime.strptime(i[5], '%Y-%m-%d %H:%M:%S.%f'))
        if i is None or i[6] == 0:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="This server has no counting stats!"
            )
            await interaction.send(embed=embed)
            return
        if i[4] == 0:
            last_user = "n/a"
        else:
            last_user = f"<@{i[4]}>"
        embed = disnake.Embed(
            color=0x8b2d27,
            title=f"Stats for {interaction.guild}",
            description=f"Current Mode: **{i[2]}**\n"
                        f"Current Count: **{i[3]}**\n"
                        f"Last User: **{last_user}**\n"
                        f"Time Since Last Count: **<t:{calendar.timegm(date.utctimetuple())}:R>**\n"
                        f"Number of Resets: **{i[6]}**\n"
                        f"High Score: **{i[7]}**\n"
                        f"Scored by **<@{i[8]}>**"
        )
        await interaction.send(embed=embed)
        return

    @counting.sub_command(
        name="user",
        description="Show the statistics for an user.",
        options=[
            Option(
                name="user",
                description="The user you want to get the stats from.",
                type=OptionType.user,
                required=True
            ),
        ],
    )
    async def server(self, interaction: ApplicationCommandInteraction, user: disnake.User):
        i = await db.stats_check_entry(interaction.guild.id, user.id)
        date = (datetime.strptime(i[5], '%Y-%m-%d %H:%M:%S.%f'))
        if i is None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="This user has no counting stats!"
            )
            await interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            color=0x8b2d27,
            title=f"Stats for {user}",
            description=f"Times Counted: **{i[2] + i[3]}**\n"
                        f"Wrong Counted: **{i[3]}**\n"
                        f"Percentual Correct: **{round(int(i[2]) / (int(i[2]) + int(i[3])) * 100, 2)}**\n"
                        f"Highest Count: **{i[4]}**\n"
                        f"Time Since Last Count: **<t:{calendar.timegm(date.utctimetuple())}:R>**"
        )
        await interaction.send(embed=embed)
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild.id
        content = message.content
        channel = message.channel.id
        author = message.author.id
        if message.author.bot:
            return
        c = await db.counting_check_entry(guild)
        if c is None:
            return
        else:
            if str(c[1]) != str(channel):
                return
            else:
                last_count = c[3]
                current_count = last_count + 1
                if c[2] == "Normal":
                    answer = helpers.check_letters(content)
                    if answer is None:
                        return
                    needed = c[3] + 1
                elif c[2] == "Fibonacci":
                    answer = helpers.check_letters(content)
                    if answer is None:
                        return
                    needed = helpers.fibonacci(last_count)
                elif c[2] == "Binary":
                    answer = helpers.check_letters(content)
                    if answer is None:
                        return
                    needed = int(format(last_count + 1, "b"))
                elif c[2] == "Roman":
                    answer = helpers.check_roman(content)
                    if answer is None:
                        return
                    needed = helpers.roman(last_count + 1)
                elif c[2] == "Letters":
                    answer = helpers.check_numbers(content)
                    if answer is None:
                        return
                    needed = helpers.letters(last_count + 1)
                else:
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Error!",
                        description="An error occurred!\nReset the current count to 0."
                    )
                    await message.channel.send(embed=embed)
                    await db.counting_update_entry(c[0], c[1], "Normal", 0, 0, (datetime.utcnow()),
                                                   c[6], c[7], c[8], c[9])
                    logging.error(f"[Counting] Exception at on_message: Could not find {c[2]}")
                    return
                if author == c[4]:
                    mode = random.choice(["Normal", "Binary", "Fibonacci", "Roman", "Letters"])
                    await db.counting_update_entry(c[0], c[1], mode, 0, 0, (datetime.utcnow()),
                                                   c[6] + 1, c[7], c[8], c[9])
                    await db.stats_update_entry(guild, author, False, current_count, datetime.utcnow())
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} was too **greedy** at {needed}!\n"
                                    f"The mode is now set to **{mode}**."
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if answer != needed:
                    mode = random.choice(["Normal", "Binary", "Fibonacci", "Roman", "Letters"])
                    await db.counting_update_entry(c[0], c[1], mode, 0, 0, (datetime.utcnow()),
                                                   c[6] + 1, c[7], c[8], c[9])
                    await db.stats_update_entry(guild, author, False, current_count, datetime.utcnow())
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} has **failed** at {needed}!\n "
                                    f"The mode is now set to **{mode}**."
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if answer == needed:
                    if c[7] < current_count:
                        await db.counting_update_entry(c[0], c[1], c[2], current_count, author, datetime.utcnow(), c[6],
                                                       current_count, author, (datetime.utcnow()))
                    else:
                        await db.counting_update_entry(c[0], c[1], c[2], current_count, author, datetime.utcnow(), c[6],
                                                       c[7], c[8], c[9])
                    await db.stats_update_entry(guild, author, True, current_count, (datetime.utcnow()))
                    if c[7] < current_count:
                        reaction = "☑"
                    elif current_count == 3:
                        reaction = "💯"
                    else:
                        reaction = "✅"
                    await message.add_reaction(reaction)
                    return


def setup(bot):
    bot.add_cog(Counting(bot))
