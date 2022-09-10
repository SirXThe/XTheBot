import disnake

from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class AvatarCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="avatar",
        description="Get the avatar from a user.",
        options=[
            Option(
                name="user",
                description="The user you want to get the avatar from.",
                type=OptionType.user,
                required=True
            )
        ]
    )
    async def avatar(self, interaction: ApplicationCommandInteraction, user) -> None:
        embed = disnake.Embed(
            title=f"User Avatar from {user}:",
            color=0x8b2d27
        )
        if user.avatar is not None:
            embed.set_image(
                url=user.avatar
            )
        else:
            embed.description = "User does not have an avatar."
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(AvatarCommand(bot))
