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

import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class EightBallCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="8ball",
        description="Ask the Magic 8-Ball a question.",
        options=[
            Option(
                name="question",
                description="The question you want to ask.",
                type=OptionType.string,
                required=True
            )
        ],
    )
    async def eightball(self, interaction: ApplicationCommandInteraction, question: str) -> None:
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.", "Don’t count on it.", "It is certain.", "It is decidedly so.",
                     "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.",
                     "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.",
                     "Yes – definitely.", "You may rely on it."]
        embed = disnake.Embed(
            title="The 8-Ball says:",
            description=f"**{random.choice(responses)}**\nYou asked: {question}",
            color=0x8b2d27
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(EightBallCommand(bot))
