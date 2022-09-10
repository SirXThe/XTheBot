import disnake
from disnake import ApplicationCommandInteraction, OptionType, Option
from disnake.ext import commands


class DeleteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(
        name="delete",
        description="Delete a number of messages.",
        options=[
            Option(
                name="amount",
                description="The number of messages you want to delete.",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def delete(self, interaction: ApplicationCommandInteraction, amount: int) -> None:
        try:
            clear = await interaction.channel.purge(limit=amount)
            if len(clear) == 1:
                embed = disnake.Embed(
                    title="Message was deleted!",
                    description=f"1 message was successfully deleted by {interaction.author}!",
                    color=0x8b2d27
                )
                embed.set_footer(
                    text="Made by XThe"
                )
            else:
                embed = disnake.Embed(
                    title="Messages were deleted!",
                    description=f"{len(clear)} messages were successfully deleted by {interaction.author}!",
                    color=0x8b2d27
                )
                embed.set_footer(
                    text="Made by XThe"
                )
            await interaction.send(embed=embed)
        except:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Error!",
                description="Could not delete all messages successfully. Maybe your amount was too big."
            )
            embed.set_footer(
                text="Made by XThe"
            )
            await interaction.send(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(DeleteCommand(bot))
