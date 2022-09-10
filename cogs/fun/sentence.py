import random

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class SentenceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="sentence",
        description="The bot will randomise your sentence.",
        options=[
            Option(
                name="sentence",
                description="The sentence you want to randomise.",
                type=OptionType.string,
                required=True
            )
        ]
    )
    async def sentence(self, interaction: ApplicationCommandInteraction, sentence: str) -> None:
        str_var = list(sentence)
        random.shuffle(str_var)
        embed = disnake.Embed(
            title=f"The randomised sentence:",
            description=f"{''.join(str_var)}",
            color=0x8b2d27
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SentenceCommand(bot))
