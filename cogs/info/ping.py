import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Show the bot latency.",
    )
    async def ping(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms."
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot))
