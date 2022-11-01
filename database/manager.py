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
from datetime import datetime
import logging


async def counting_new_entry(guild_id: int, channel_id: int, mode: str, count: int = 0,
                             last_user: int = 0, last_counted: int = 0, resets: int = 0,
                             record: int = 0, record_user: int = 0, record_time: int = 0):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO counting(guild_id, channel_id, mode, count, last_user, "
                         "last_counted, resets, record, record_user, record_time "
                         ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (guild_id, channel_id, mode, count, last_user, last_counted, resets, record,
                          record_user, record_time))
        await db.commit()
        logging.info(f"[Counting] Created guild entry for {guild_id}, set it to {channel_id}")


async def counting_check_entry(guild_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM counting WHERE guild_id=?", (guild_id,)) as cursor:
            result = await cursor.fetchone()
            return result


async def counting_update_entry(guild_id: int, channel_id: int, mode: str, count: int,
                                last_user: int, last_counted: datetime, resets: int,
                                record: int, record_user: int, record_time: datetime):
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("UPDATE counting SET guild_id = ?, channel_id = ?, mode = ?, count = ?,"
                         "last_user = ?, last_counted = ?, resets = ?, "
                         "record = ?, record_user = ?, record_time = ? WHERE guild_id = ?",
                         (guild_id, channel_id, mode, count, last_user, last_counted, resets, record,
                          record_user, record_time, guild_id))
        await db.commit()
        logging.info(f"[Counting] Updated counting entry for {guild_id}, set it to {channel_id}, {count}, {last_user},"
                     f"{resets}, {record}, {record_user}")


async def stats_update_entry(guild_id: int, user_id: int, correct: bool, current_count: int, last_counted: datetime):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM stats WHERE guild_id='{guild_id}' AND user_id='{user_id}'") as cursor:
            result = await cursor.fetchone()
            print(result)
            if result is None:
                await db.execute("INSERT INTO stats(guild_id, user_id, correct, wrong, highest, last_counted)"
                                 "VALUES (?, ?, ?, ?, ?, ?)",
                                 (guild_id, user_id, 0, 0, 0, 0))
                await db.commit()
                return
            else:
                if result[4] < current_count:
                    highest = current_count
                else:
                    highest = result[4]
                if correct:
                    await db.execute("UPDATE stats SET guild_id = ?, user_id = ?, correct = ?, wrong = ?, highest = ?,"
                                     "last_counted= ?"
                                     "WHERE guild_id = ? AND user_id = ?",
                                     (guild_id, user_id, result[2] + 1, result[3], highest, last_counted, guild_id,
                                      user_id))
                    print("True")
                else:
                    await db.execute(f"UPDATE stats SET guild_id = ?, user_id = ?, correct = ?, wrong = ?,"
                                     f"last_counted = ?"
                                     " WHERE guild_id = ? AND user_id = ?",
                                     (guild_id, user_id, result[2], result[3] + 1, last_counted, guild_id, user_id))
                    print("Wrong")
                await db.commit()
                return


async def stats_check_entry(guild_id: int, user_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM stats WHERE guild_id='{guild_id}' AND user_id='{user_id}'") as cursor:
            result = await cursor.fetchone()
            return result
