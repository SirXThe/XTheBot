import disnake
from disnake import Option, OptionType, ApplicationCommandInteraction
from disnake.ext import commands


class EmbedCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="embed",
        description="Generate a custom embed message.",
        options=[
            Option(
                name="message",
                description="The message of your embed.",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="title",
                description="The title of your embed.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="footer",
                description="The footer of your embed.",
                type=OptionType.string,
                required=False
            ),
            Option(
                name="color",
                description="The color of your embed.",
                type=OptionType.string,
                required=False,
                choices=["teal", "dark_teal", "green", "dark_green", "blue", "dark_blue", "purple", "dark_purple",
                         "magenta", "dark_magenta", "gold", "dark_gold", "orange", "dark_orange", "red", "dark_red",
                         "lighter_grey", "dark_grey", "light_grey", "darker_grey", "blurple", "greyple"]
            ),
        ],
    )
    async def embed(self, interaction: ApplicationCommandInteraction, message: str, title: str = "",
                    footer: str = "", color: disnake.Colour = 0x8b2d27) -> None:
        embed = disnake.Embed(
            title=title,
            description=message,
            color=color
        )
        embed.set_footer(
            text=footer
        )
        await interaction.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(EmbedCommand(bot))
