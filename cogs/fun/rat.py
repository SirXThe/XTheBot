from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class RatCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="rat",
        description="Show the picture of a rat."
    )
    async def rat(self, interaction: ApplicationCommandInteraction) -> None:
        url: str = "https://bigrat.monster"
        await interaction.send(url)


def setup(bot: commands.Bot):
    bot.add_cog(RatCommand(bot))
