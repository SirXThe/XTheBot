import disnake
from disnake import Option, OptionType, ApplicationCommandInteraction
from disnake.ext import commands


class NickCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        name="nick",
        description="Nick a user in the server.",
        options=[
            Option(
                name="user",
                description="The user you want to nick.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="name",
                description="The new name for the user.",
                type=OptionType.string,
                required=True
            ),
        ],
    )
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   name: str) -> None:
        user = await interaction.guild.get_or_fetch_member(user.id)
        try:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="**A User got nicked!**",
                description=f"The user **{user.mention}** has been nicked by **{interaction.author}**"
                            f"\n New name: **{name}**"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await user.edit(nick=name)
            await interaction.send(embed=embed)
        except disnake.Forbidden:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not nick the user. Make sure the user isn't Admin or my role is above the user."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(NickCommand(bot))
