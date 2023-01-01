#  XTheBot - A multifunctional bot for Discord.
#  Copyright (C) 2022 - 2023  XThe
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class RulesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        dm_permission=False,
        name="rules",
        description="Show a server rules template."
    )
    @commands.has_permissions(administrator=True)
    async def rules(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            title=f"Server rules for {interaction.guild}",
            description="**1. Be respectful**\n You must respect all users, regardless of your liking towards them. "
                        "Treat others the way you want to be treated.\n \n **2. No Inappropriate Language**\n The use "
                        "of profanity should be kept to a minimum. However, any derogatory language towards any user "
                        "is prohibited.\n \n **3. No spamming**\n Don't send a lot of small messages right after each "
                        "other. Do not disrupt chat by spamming.\n \n **4. No pornographic/adult/other NSFW "
                        "material**\n This is a community server and not meant to share this kind of material.\n \n "
                        "**5. No advertisements**\n We do not tolerate any kind of advertisements, whether it be for "
                        "other communities or streams. You can post your content in the media channel if it is "
                        "relevant and provides actual value (Video/Art).\n \n **6. No offensive names and profile "
                        "pictures**\n You will be asked to change your name or picture if the staff deems them "
                        "inappropriate.\n \n **7. Server Raiding**\n Raiding or mentions of raiding are not "
                        "allowed.\n \n **8. Direct & Indirect Threats**\n Threats to other users of DDoS, Death, DoX, "
                        "abuse, and other malicious threats are absolutely prohibited and disallowed.\n \n **9. "
                        "Follow the Discord Community Guidelines**\n You can find them here: "
                        "https://discordapp.com/guidelines\n \n **10. Do not join voice chat channels without "
                        "permission of the people already in there**\n If you see that they have a free spot it is "
                        "alright to join and ask whether they have an open spot, but leave if your presence is not "
                        "wanted by whoever was there first.\n \n **The Admins and Mods will Mute/Kick/Ban per "
                        "discretion. If you feel mistreated dm an Admin and we will resolve the issue.**",
            color=0x8b2d27
        )
        embed.set_footer(
            text="Made by XThe"
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(RulesCommand(bot))
