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
from disnake.ext import commands, tasks
from os.path import sep, join

import random
import glob
import json
import platform
import os
import sys

intents = disnake.Intents.default()
bot = commands.Bot(intents=intents)

if not os.path.isfile("settings.json"):
    sys.exit("An error occurred initializing the settings.json file!")
else:
    with open("settings.json") as file:
        settings = json.load(file)

bot.settings = settings


@bot.event
async def on_ready() -> None:
    await bot.change_presence(status=disnake.Status.online)
    await setup()
    await status.start()
    print("-----------------------------")
    print(f"Logged in as {bot.user.name}")
    print(f"Bot version: {settings['version']}")
    print(f"Disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-----------------------------")


async def setup() -> None:
    for path, subdirs, files in os.walk('cogs'):
        for name in files:
            file_name: str = (os.path.join(path, name)).replace("\\", ".")
            if file_name.endswith(".py"):
                extension = file_name[:-3]
                try:
                    bot.load_extension(f"{extension}")
                    print(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to load extension {extension}\n{exception}")


@tasks.loop(minutes=1.0)
async def status() -> None:
    await bot.change_presence(activity=disnake.Game(random.choice(settings["status"])))

bot.run(settings["token"])
