import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class SupportCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="support",
        description="Get the invitation link for the support server.",
    )
    async def support(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            color=0x8b2d27,
            title="The link to the support server:",
            description="https://discord.gg/udTcwmMnqS"
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SupportCommand(bot))
