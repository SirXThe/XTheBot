import disnake
from disnake.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        channel = member.guild.system_channel
        if channel is not None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Member Joined!",
                description=f"**{member}** joined the server. There are now **{channel.guild.member_count}**"
                            f" members."
            )
            try:
                await channel.send(embed=embed)
                embed = disnake.Embed(
                    color=0x8b2d27,
                    title=f"Thanks for joining {channel.guild}!"
                )
                await member.send(embed=embed)
            except:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member) -> None:
        channel = member.guild.system_channel
        if channel is not None:
            embed = disnake.Embed(
                color=0x8b2d27,
                title="Member Left!",
                description=f"**{member}** left the server. There are now **{channel.guild.member_count}**"
                            f" members."
            )
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
