"""
XTheBot
Copyright (C) 2022  XThe

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import disnake
from disnake.ext import commands

import settings
import platform
import os

intents = disnake.Intents.default()
intents.message_content = True
intents.members = True

extensions: list = ["cogs.welcome", "cogs.moderation.mention", "cogs.moderation.rules",
                    "cogs.fun.8ball", "cogs.fun.sentence", "cogs.fun.facts", "cogs.fun.joke",
                    "cogs.fun.bitcoin", "cogs.fun.coinflip", "cogs.fun.rps", "cogs.fun.digit",
                    "cogs.fun.rat", "cogs.fun.raccoon", "cogs.fun.bored", "cogs.info.avatar",
                    "cogs.fun.google", "cogs.fun.embed", "cogs.info.ping",
                    "cogs.info.serverinfo", "cogs.info.botinfo", "cogs.info.invite", "cogs.info.support",
                    "cogs.moderation.ban", "cogs.moderation.kick", "cogs.moderation.nick",
                    "cogs.moderation.delete", "cogs.moderation.warn", "cogs.moderation.timeout"]

bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game(settings.BotStatus))
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except Exception as exc:
            error = "{}: {}".format(type(exc).__name__, exc)
            print("Failed to load extension {}\n{}".format(extension, error))
    print("-----------------------------")
    print(f"Logged in as {bot.user.name}")
    print(f"Bot version: {settings.Version}")
    print(f"Disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-----------------------------")


bot.run(settings.TOKEN)
