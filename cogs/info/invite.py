import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class InviteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="invite",
        description="Invite the bot to your server.",
    )
    async def invite(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            color=0x8b2d27,
            title="Error!",
            description="The bot hasn't been released to the public (yet)."
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(InviteCommand(bot))
