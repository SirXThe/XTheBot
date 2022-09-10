import disnake
from disnake import Option, OptionType, ApplicationCommandInteraction
from disnake.ext import commands


class BanCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        dm_permission=False,
        name="ban",
        description="Ban a user from the server.",
        options=[
            Option(
                name="user",
                description="The user you want to ban.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="reason",
                description="The reason why you want to ban the user.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="messages",
                description="The number of days worth of messages to delete from the user in the server.",
                type=OptionType.integer,
                required=False,
                min_value=0,
                max_value=7
            ),
        ],
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                  reason: str = "No reason provided", messages: int = 0) -> None:
        user = await interaction.guild.get_or_fetch_member(user.id)
        try:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="**A User got banned!**",
                description=f"The user **{user}** has been banned by **{interaction.author}**."
                            f"\n Reason: **{reason}**"
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await user.ban(reason=reason, delete_message_days=messages)
            await interaction.send(embed=embed)

        except disnake.Forbidden:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not ban the user. Make sure the user isn't owner and my role is above the user."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(BanCommand(bot))
