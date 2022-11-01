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

from database import manager as db
from helpers import helpers
import logging
import random
import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


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
                name="channel_id",
                description="Insert the channel id or leave it blank if you want to use the current channel.",
                type=OptionType.integer,
                required=False
            ),
        ],
    )
    async def counting_setup(self, interaction: ApplicationCommandInteraction, channel_id: int = None):
        if channel_id is None:
            channel_id = interaction.channel.id
        c = await db.counting_check_entry(interaction.guild.id)
        if c is None:
            await db.counting_new_entry(interaction.guild.id, channel_id, "normal")
        else:
            await db.counting_update_entry(interaction.guild.id, channel_id, c[2], c[3],
                                           c[4], c[5], c[6], c[7], c[8], c[9], c[10])
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Updated Channel ID!",
            description=f"Updated channel ID to {channel_id}!"
        )
        await interaction.send(embed=embed)

    @counting.sub_command(
        name="server",
        description="Show the statistics for the current server."
    )
    async def server(self, interaction: ApplicationCommandInteraction):
        i = await db.counting_check_entry(interaction.guild.id)
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
            last_user = f"<@{i[3]}>"
        embed = disnake.Embed(
            color=0x8b2d27,
            title=f"Stats for {interaction.guild}",
            description=f"Current count: {i[2]}\n"
                        f"Last user: {last_user}\n"
                        f"Number of resets: {i[4]}\n"
                        f"High score: {i[5]}\n"
                        f"Scored by <@{i[6]}>"
        )
        await interaction.send(embed=embed)
        return

    @counting.sub_command(
        name="user",
        description="Show the statistics for an user.",
        options=[
            Option(
                name="user_id",
                description="The user you want to get the stats from.",
                type=OptionType.user,
                required=True
            ),
        ],
    )
    async def server(self, interaction: ApplicationCommandInteraction, user_id: disnake.User):
        i = await db.stats_check_entry(interaction.guild.id, user_id.id)
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
            title=f"Stats for {user_id}",
            description=f"Right counted: {i[2]}\n"
                        f"Wrong counted: {i[3]}\n"
                        f"Percentual correct: {round(int(i[2]) / (int(i[2]) + int(i[3])) * 100, 2)}\n"
                        f"Highest count: {i[4]}\n"
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
                commit = last_count + 1
                if c[2] == "normal":
                    answer = helpers.check_letters(content)
                    if answer is None:
                        return
                    needed = c[3] + 1
                elif c[2] == "fibonacci":
                    answer = helpers.check_letters(content)
                    if answer is None:
                        return
                    needed = helpers.fibonacci(last_count)
                elif c[2] == "binary":
                    answer = helpers.check_letters(content)
                    if answer is None:
                        return
                    needed = int(format(last_count + 1, "b"))
                elif c[2] == "roman":
                    answer = helpers.check_roman(content)
                    if answer is None:
                        return
                    needed = helpers.roman(last_count + 1)
                elif c[2] == "letters":
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
                    await db.counting_update_entry(c[0], c[1], c[2], 0, 42, 0, 0, c[7], c[8], c[9], c[10])
                    logging.error(f"[Counting] Exception at on_message: Could not find {c[2]}")
                    return
                if author == c[5]:
                    mode = random.choice(["normal", "binary", "fibonacci", "roman", "letters"])
                    await db.counting_update_entry(c[0], c[1], mode, 0, 42, 0, 0, c[7] + 1, c[8], c[9], c[10])
                    await db.stats_update_entry(guild, author, False, commit)
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
                    mode = random.choice(["normal", "binary", "fibonacci", "roman", "letters"])
                    await db.counting_update_entry(c[0], c[1], mode, 0, 42, 0, 0, c[7] + 1, c[8], c[9], c[10])
                    await db.stats_update_entry(guild, author, False, commit)
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
                    if c[8] < commit:
                        await db.counting_update_entry(c[0], c[1], c[2], commit, 42, author, 0, c[7],
                                                       commit, author, c[10])
                    else:
                        await db.counting_update_entry(c[0], c[1], c[2], commit, 42, author, 0, c[7], c[8],
                                                       c[9], c[10])
                    await db.stats_update_entry(guild, author, True, commit)
                    if commit == 100:
                        reaction = "💯"
                    else:
                        reaction = "✅"
                    await message.add_reaction(reaction)
                    return


def setup(bot):
    bot.add_cog(Counting(bot))
