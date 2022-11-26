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

import json
import logging
import os
import platform
import random
import sqlite3
import sys
from os.path import sep

import aiohttp
import aiosqlite
import disnake
from disnake.ext import commands, tasks

logging.basicConfig(filename='bot.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m-%d-%Y %H:%M:%S',
                    encoding='utf-8', filemode='w', level=logging.INFO)
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)

if not os.path.isfile("settings.json"):
    logging.critical("Could not find the settings.json file!")
    sys.exit("An error occurred initializing the settings.json file!")
else:
    with open("settings.json", "r") as file:
        settings = json.load(file)
        logging.info("Loaded the settings.json file")
        bot.settings = settings


@bot.event
async def on_ready() -> None:
    await bot.change_presence(status=disnake.Status.online)
    await get_api()
    await status()
    await create_db()
    # await setup()
    bot.load_extension("cogs.counting.counting")
    print("-----------------------------")
    print(f"Logged in as {bot.user.name}")
    print(f"Bot version: {settings['version']}")
    print(f"SQLite version: {sqlite3.version}")
    print(f"Disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-----------------------------")


async def get_api() -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://xthe.me/XTheBotAPI/index.json") as request:
            if request.status == 200:
                data = await request.json()
                bot.data = data
                with open('data.json', 'w') as f:
                    f.write(json.dumps(data))
                    logging.info(f"Loaded the bot API from {request}")
            else:
                logging.critical(f"Could not access the API! Tried {request}")
                sys.exit("Error: Could not access the API. Try again later!")


async def create_db() -> None:
    async with aiosqlite.connect("database/database.db") as db:
        with open("database/setup.sql", "r") as f:
            await db.executescript(f.read())
        await db.commit()


async def setup() -> None:
    for path, subdirs, files in os.walk('cogs'):
        for name in files:
            file_name: str = (os.path.join(path, name)).replace(sep, ".")
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
