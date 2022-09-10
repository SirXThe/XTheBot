import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class JokeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="joke",
        description="Show a random joke.",
    )
    async def joke(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist&type=single") \
                    as request:
                if request.status == 200:
                    json = await request.json(
                        content_type="application/json")
                    embed = disnake.Embed(
                        description=json["joke"],
                        color=0x8b2d27
                    )
                    embed.set_footer(
                        text="Made by XThe"
                    )
                    await interaction.send(embed=embed)
                else:
                    embed = disnake.Embed(
                        title="Error!",
                        description="The API did not respond, try again later.",
                        color=0x8b2d27
                    )
                    embed.set_footer(
                        text="Made by XThe"
                    )
                    await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(JokeCommand(bot))
