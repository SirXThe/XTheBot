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
import sympy
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
            await db.counting_new_entry(interaction.guild.id, channel_id)

        else:
            await db.counting_update_entry(interaction.guild.id, channel_id, c[2], c[3],
                                           c[4], c[5], c[6])
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
                try:
                    if any(a.isalpha() for a in content):
                        return
                    else:
                        current_count = int(sympy.sympify(content))
                except Exception:
                    return
                old_count = c[2]
                if author == c[3]:
                    await db.counting_update_entry(c[0], c[1], 0, 0, c[4] + 1, c[5], c[6])
                    await db.stats_update_entry(guild, author, False, current_count)
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} was too **greedy!**"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if old_count + 1 != current_count:
                    await db.counting_update_entry(c[0], c[1], 0, 0, c[4] + 1, c[5], c[6])
                    await db.stats_update_entry(guild, author, False, current_count)
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} has **failed** at {old_count + 1}!\n Answer: "
                                    f"{current_count}"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if old_count + 1 == current_count:
                    if c[5] < current_count:
                        await db.counting_update_entry(c[0], c[1], current_count, author, c[4],
                                                       current_count, author)
                    else:
                        await db.counting_update_entry(c[0], c[1], current_count, author,
                                                       c[4], c[5], c[6])
                    await db.stats_update_entry(guild, author, True, current_count)
                    if current_count == 100:
                        reaction = "💯"
                    else:
                        reaction = "✅"
                    await message.add_reaction(reaction)
                    return


def setup(bot):
    bot.add_cog(Counting(bot))
