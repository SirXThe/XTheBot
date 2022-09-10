from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class RaccoonCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="raccoon",
        description="Show the picture of a raccoon."
    )
    async def raccoon(self, interaction: ApplicationCommandInteraction) -> None:
        url: str = "https://bigraccoon.monster"
        await interaction.send(url)


def setup(bot: commands.Bot):
    bot.add_cog(RaccoonCommand(bot))
