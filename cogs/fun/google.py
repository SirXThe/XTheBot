import googlesearch
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class GoogleCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="google",
        description="Search something in the world wide web with Google.",
        options=[
            Option(
                name="query",
                description="What do you want to search.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="language",
                description="",
                type=OptionType.string,
                required=True,
                choices=["en", "de", "fr"]
            ),
        ],
    )
    async def google(self, interaction: ApplicationCommandInteraction, query: str, language: str = "en") -> None:
        for result in googlesearch.search(query, num_results=1, lang=language):
            await interaction.send(result)
            break


def setup(bot: commands.Bot):
    bot.add_cog(GoogleCommand(bot))
