import platform

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

import settings


class BotInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Show some information about the bot."
    )
    async def botinfo(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Information about the XTheBot.",
            description="**Owners:**\n"
                        "**XThe#4695** and **HugoOV#0979**\n"
                        "**Prefix:**\n"
                        "Slash Commands (/)\n"
                        "**Bot Version:**\n"
                        f"{settings.Version}\n"
                        "**Python Version:**\n"
                        f"{platform.python_version()}\n"
                        "**Disnake API Version:**\n"
                        f"{disnake.__version__}\n"
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(BotInfoCommand(bot))
