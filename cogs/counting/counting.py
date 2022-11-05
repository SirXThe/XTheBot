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

import calendar
import logging
import random
from datetime import datetime

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType, ChannelType
from disnake.ext import commands

from database import manager as db
from helpers import counting_helpers as helpers


class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang = bot.data['counting']

    @commands.slash_command(
        dm_permission=False,
        name="counting"
    )
    async def counting(self, interaction: ApplicationCommandInteraction):
        pass

    @commands.has_permissions(administrator=True)
    @counting.sub_command(
        name="setup",
        description="[Admin] Setup the counting function.",
        options=[
            Option(
                name="channel",
                description="Select your counting channel (Text Channel only!).",
                type=OptionType.channel,
                required=True
            ),
        ],
    )
    async def setup(self, interaction: ApplicationCommandInteraction, channel: disnake.TextChannel):
        if not channel.type == ChannelType.text or not ChannelType.news:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description=f"Please select a text channel!"
            )
            await interaction.send(embed=embed, ephemeral=True)
            return
        i = await db.counting_check_entry(interaction.guild.id)
        mode = "Normal"
        if i is None:
            await db.counting_new_entry(interaction.guild.id, channel.id)
        else:
            await db.counting_update_entry(interaction.guild.id, channel.id, mode, i[3], i[4], i[5], i[6], i[7],
                                           i[8], i[9])
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Updated Channel!",
            description=f"Updated channel to {channel.mention}!\n"
                        f"The counting mode is now set to **{mode}**.\n"
                        f"{self.lang[mode]}"
        )
        await interaction.send(embed=embed)
        if not interaction.channel.id == channel.id:
            await channel.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @counting.sub_command(
        name="mode",
        description="[Admin] Change the current counting mode and reset the current count to 0.",
        options=[
            Option(
                name="mode",
                description="Select the mode you want to use.",
                type=OptionType.string,
                required=True,
                choices=["Normal", "Binary", "Fibonacci", "Roman", "Alphabet"]
            ),
        ],
    )
    async def mode(self, interaction: ApplicationCommandInteraction, mode: str):
        i = await db.counting_check_entry(interaction.guild.id)
        if i is None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="This server has no counting entry!\n"
                            "If you want to setup the counting function, run **/counting setup** first!"
            )
            await interaction.send(embed=embed, ephemeral=True)
            return
        else:
            await db.counting_update_entry(i[0], i[1], mode, 0, 0, datetime.utcnow(), i[6], i[7], i[8], i[9])
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Updated Mode!",
                description=f"Set the mode to **{mode}** and reset the current count to 0.\n"
                            f"{self.lang[mode]}"
            )
            await interaction.send(embed=embed)
            if interaction.channel.id == i[1]:
                return
            else:
                channel = interaction.guild.get_channel(i[1])
                await channel.send(embed=embed)
                return

    @counting.sub_command(
        name="server",
        description="Show the statistics for the current server."
    )
    async def server(self, interaction: ApplicationCommandInteraction):
        i = await db.counting_check_entry(interaction.guild.id)
        if i is None or i[7] == 0:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="This server has no counting stats!"
            )
            await interaction.send(embed=embed, ephemeral=True)
            return
        if i[4] == 0:
            last_user = "n/a"
        else:
            last_user = f"<@{i[4]}>"
        date = (datetime.strptime(str(i[5]), '%Y-%m-%d %H:%M:%S.%f'))
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
    async def user(self, interaction: ApplicationCommandInteraction, user: disnake.User):
        i = await db.stats_check_entry(interaction.guild.id, user.id)
        if i is None or i[4] == 0:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="This user has no counting stats!"
            )
            await interaction.send(embed=embed, ephemeral=True)
            return
        else:
            date = (datetime.strptime(str(i[5]), '%Y-%m-%d %H:%M:%S.%f'))
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

    @counting.sub_command(
        name="delete",
        description="Delete your counting data."
    )
    async def delete(self, interaction: ApplicationCommandInteraction):
        i = await db.stats_check_entry(interaction.guild.id, interaction.user.id)
        if i is None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="You need to count first!"
            )
            await interaction.send(embed=embed, ephemeral=True)
        else:
            await db.stats_delete_entry(interaction.guild.id, interaction.user.id)
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Success!",
                description=f"Deleted your data from **{interaction.guild}**."
            )
            await interaction.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild.id
        content = message.content
        channel = message.channel.id
        author = message.author.id
        if message.author.bot:
            return
        i = await db.counting_check_entry(guild)
        if i is None:
            return
        else:
            if str(i[1]) != str(channel):
                return
            else:
                last_count = i[3]
                current_count = last_count + 1
                if i[2] == "Normal":
                    answer = helpers.containsLetter(content)
                    if answer is None:
                        return
                    needed = i[3] + 1
                elif i[2] == "Fibonacci":
                    answer = helpers.containsLetter(content)
                    if answer is None:
                        return
                    needed = helpers.Fibonacci(last_count + 1)
                elif i[2] == "Binary":
                    answer = helpers.containsLetter(content)
                    if answer is None:
                        return
                    needed = int(format(last_count + 1, "b"))
                elif i[2] == "Roman":
                    answer = helpers.isRoman(content)
                    if answer is None:
                        return
                    needed = helpers.Roman(last_count + 1)
                elif i[2] == "Alphabet":
                    answer = helpers.containsNumber(content)
                    if answer is None:
                        return
                    needed = helpers.Letter(last_count + 1)
                else:
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Error!",
                        description="An error occurred!\n"
                                    "Reset the current count to 0."
                    )
                    await message.channel.send(embed=embed)
                    await db.counting_update_entry(i[0], i[1], "Normal", 0, 0, (datetime.utcnow()),
                                                   i[6], i[7], i[8], i[9])
                    logging.error(f"[Counting] Exception at on_message: Could not find {i[2]}")
                    return
                if author == i[4] and last_count != 0:
                    mode = random.choice(["Normal", "Binary", "Fibonacci", "Roman", "Alphabet"])
                    await db.counting_update_entry(i[0], i[1], mode, 0, 0, (datetime.utcnow()),
                                                   i[6] + 1, i[7], i[8], i[9])
                    await db.stats_update_entry(guild, author, False, current_count, datetime.utcnow())
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} was too **greedy** at {needed}!\n"
                                    f"The mode is now set to **{mode}**.\n"
                                    f"{self.lang[mode]}"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if answer != needed and last_count != 0:
                    mode = random.choice(["Normal", "Binary", "Fibonacci", "Roman", "Alphabet"])
                    await db.counting_update_entry(i[0], i[1], mode, 0, 0, (datetime.utcnow()),
                                                   i[6] + 1, i[7], i[8], i[9])
                    await db.stats_update_entry(guild, author, False, current_count, (datetime.utcnow()))
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} has **failed** at {needed}!\n "
                                    f"The mode is now set to **{mode}**.\n"
                                    f"{self.lang[mode]}"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if answer != needed and last_count == 0:
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Warning!",
                        description=f"The next count is **{needed}**!",
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("⚠")
                    return
                if answer == needed:
                    if i[7] < current_count:
                        await db.counting_update_entry(i[0], i[1], i[2], current_count, author, datetime.utcnow(), i[6],
                                                       current_count, author, (datetime.utcnow()))
                    else:
                        await db.counting_update_entry(i[0], i[1], i[2], current_count, author, datetime.utcnow(), i[6],
                                                       i[7], i[8], i[9])
                    await db.stats_update_entry(guild, author, True, current_count, (datetime.utcnow()))
                    if i[7] < current_count:
                        reaction = "☑"
                    else:
                        reaction = "✅"
                    if current_count == 42:
                        reaction = ["🤔"]
                    elif current_count == 100:
                        reaction = ["💯"]
                    elif current_count == 333:
                        reaction = ["🔺", "👁"]
                    elif current_count == 666:
                        reaction = ["👹"]
                    elif current_count == 1234:
                        reaction = ['🔢']
                    for r in reaction:
                        await message.add_reaction(r)
                    return


def setup(bot):
    bot.add_cog(Counting(bot))
