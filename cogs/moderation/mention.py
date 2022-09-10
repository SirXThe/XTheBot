from random import choice

from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class MentionCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="mention",
        description="Mentions a random user."
    )
    @commands.has_permissions(administrator=True)
    async def mention(self, interaction: ApplicationCommandInteraction) -> None:
        user = choice(interaction.channel.guild.members)
        await interaction.send(f"{user.mention}")


def setup(bot: commands.Bot):
    bot.add_cog(MentionCommand(bot))
