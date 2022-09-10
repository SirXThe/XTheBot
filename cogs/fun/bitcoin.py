import aiohttp
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class BitcoinCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="bitcoin",
        description="Show the current price of bitcoin.",
    )
    async def bitcoin(self, interaction: ApplicationCommandInteraction) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coinlore.net/api/ticker/?id=90") as request:
                if request.status == 200:
                    json = await request.json()
                    price = json[0]["price_usd"]
                    embed = disnake.Embed(
                        title="The current bitcoin price:",
                        description=f"{price} US-Dollar",
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
    bot.add_cog(BitcoinCommand(bot))
