import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class RandomFactCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="fact",
        description="Show a random fact."
    )
    async def facts(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    json = await request.json()
                    embed = disnake.Embed(
                        description=json["text"],
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
    bot.add_cog(RandomFactCommand(bot))
