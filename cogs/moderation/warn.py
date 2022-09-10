import disnake
from disnake import Option, OptionType, ApplicationCommandInteraction
from disnake.ext import commands


class WarnCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        name="warn",
        description="Warn a user in the server.",
        options=[
            Option(
                name="user",
                description="The user you want to warn.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason why you want to warn the user.",
                type=OptionType.string,
                required=False
            ),
        ],
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                   reason: str = "No reason provided") -> None:
        user = await interaction.guild.get_or_fetch_member(user.id)
        try:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="**A User got warned!**",
                description=f"The user **{user.mention}** has been warned by **{interaction.author}**."
                            f"\n Reason: **{reason}**"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed)

        except disnake.Forbidden:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not warn the user. Make sure the user isn't owner and my role is above the user."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(WarnCommand(bot))
