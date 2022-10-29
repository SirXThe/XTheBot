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

import aiosqlite
import logging


async def counting_new_entry(guild_id: int, channel_id: int, count: int = 0, last_user: int = 0):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO counting(guild_id, channel_id, count, last_user) VALUES (?, ?, ?, ?)",
                         (guild_id, channel_id, count, last_user,))
        await db.commit()
        logging.info(f"[Counting] Created guild entry for {guild_id}, set it to {channel_id}")


async def counting_check_entry(guild_id):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM counting WHERE guild_id=?", (guild_id,)) as cursor:
            result = await cursor.fetchone()
            return result


async def counting_update_entry(guild_id: int, channel_id: int, count: int, last_user: int):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("UPDATE counting SET guild_id = ?, channel_id = ?, count = ?, last_user = ? WHERE guild_id = "
                         "'%s'" %
                         guild_id, (guild_id, channel_id, count, last_user))
        await db.commit()
        logging.info(f"[Counting] Updated counting entry for {guild_id}, set it to {channel_id}, {count}, {last_user}")
