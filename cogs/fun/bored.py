import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class BoredCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="bored",
        description="Show some tips you can do when you are bored.",
    )
    async def bored(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.boredapi.com/api/activity") as request:
                if request.status == 200:
                    json = await request.json(
                        content_type="application/json")
                    embed = disnake.Embed(
                        description=json["activity"],
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
    bot.add_cog(BoredCommand(bot))
