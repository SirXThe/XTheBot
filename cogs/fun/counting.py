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
        name="counting_setup",
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
        check = await db.counting_check_entry(interaction.guild.id)
        if check is None:
            await db.counting_new_entry(interaction.guild.id, channel_id)
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Updated Channel ID!",
                description=f"Updated channel ID to {channel_id}!"
            )
            await interaction.send(embed=embed)
        else:
            await db.counting_update_entry(interaction.guild.id, channel_id, 0, 0)

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild.id
        content = message.content
        channel = message.channel.id
        author = message.author.id
        if message.author.bot:
            return
        check = await db.counting_check_entry(guild)
        if check is None:
            return
        else:
            if str(check[1]) != str(channel):
                return
            else:
                try:
                    if any(c.isalpha() for c in content):
                        return
                    else:
                        current_count = int(sympy.sympify(content))
                except Exception:
                    return
                old_count = check[2]
                if author == check[3]:
                    await db.counting_update_entry(guild, channel, 0, 0)
                    embed = disnake.Embed(
                        color=0x8b2d27,
                        title="Fail!",
                        description=f"{message.author.mention} was too **greedy!**"
                    )
                    await message.channel.send(embed=embed)
                    await message.add_reaction("❌")
                    return
                if old_count + 1 != current_count:
                    await db.counting_update_entry(guild, channel, 0, 0)
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
                    await db.counting_update_entry(guild, channel, current_count, author)
                    if current_count == 100:
                        reaction = "💯"
                    else:
                        reaction = "✅"
                    await message.add_reaction(reaction)
                    return

def setup(bot):
    bot.add_cog(Counting(bot))
