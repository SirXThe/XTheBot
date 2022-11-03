#  XTheBot
#  Copyright (C) 2022  XThe
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
from disnake.ext import commands, tasks

import random
import logging
import sqlite3
import aiosqlite
import json
import platform
import os
import sys


logging.basicConfig(filename='bot.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m-%d-%Y %H:%M:%S',
                    encoding='utf-8', filemode='w', level=logging.INFO)
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)

if not os.path.isfile("settings.json"):
    sys.exit("An error occurred initializing the settings.json file!")
else:
    with open("settings.json") as file:
        settings = json.load(file)


@bot.event
async def on_ready() -> None:
    await bot.change_presence(status=disnake.Status.online)
    await status()
    await create_db()
    # await setup()
    try:
        bot.load_extension(f"cogs.counting.counting")
        print(f"Loaded extension cogs.fun.counting")
    except Exception as e:
        exception = f"{type(e).__name__}: {e}"
        print(f"Failed to load extension\n{exception}")
    print("-----------------------------")
    print(f"Logged in as {bot.user.name}")
    print(f"Bot version: {settings['version']}")
    print(f"SQLite version: {sqlite3.version}")
    print(f"Disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-----------------------------")


async def create_db():
    async with aiosqlite.connect("database/database.db") as db:
        with open("database/setup.sql", "r") as f:
            await db.executescript(f.read())
        await db.commit()


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
