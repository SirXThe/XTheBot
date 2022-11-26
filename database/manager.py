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

import logging
from datetime import datetime

import aiosqlite


async def counting_check_entry(guild_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM counting WHERE guild_id=?", (guild_id,)) as cursor:
            result = await cursor.fetchone()
            return result


async def counting_new_entry(guild_id: int, channel_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting WHERE guild_id='{guild_id}'") as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO counting(guild_id, channel_id, mode, count, last_user,"
                                 "last_counted, resets, record, record_user, record_time"
                                 ") VALUES (?, ?, ?, 0, 0, 0, 0, 0, 0, 0)",
                                 (guild_id, channel_id, "Normal"))
                logging.info(f"[Counting] Created guild entry for {guild_id}, set it to {channel_id}")
            await db.commit()
            return


async def counting_update_entry(guild_id: int, channel_id: int, mode: str, count: int,
                                last_user: int, last_counted: datetime, resets: int,
                                record: int, record_user: int, record_time: datetime):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting WHERE guild_id='{guild_id}'") as cursor:
            result = await cursor.fetchone()
            if result is not None:
                await db.execute("UPDATE counting SET guild_id = ?, channel_id = ?, mode = ?, count = ?,"
                                 "last_user = ?, last_counted = ?, resets = ?, "
                                 "record = ?, record_user = ?, record_time = ? WHERE guild_id = ?",
                                 (guild_id, channel_id, mode, count, last_user, last_counted, resets, record,
                                  record_user, record_time, guild_id))
                logging.info(f"[Counting] Updated counting entry for {guild_id}, set it to {channel_id}, {mode}, "
                             f"{count}, {last_user}, {last_counted}, {resets}, {record}, {record_user}, {record_time}")
            await db.commit()
            return


async def stats_update_entry(guild_id: int, user_id: int, correct: bool, current_count: int, last_counted: datetime):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting_stats WHERE guild_id='{guild_id}' AND user_id='{user_id}'") as \
                cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO counting_stats(guild_id, user_id, correct, wrong, highest, last_counted)"
                                 "VALUES (?, ?, ?, ?, ?, ?)",
                                 (guild_id, user_id, 0, 0, 0, 0))
                logging.info(f"[Counting] Created stats entry for {guild_id} and {user_id}")
                await db.commit()
                return
            else:
                if result[4] < current_count:
                    highest = current_count
                else:
                    highest = result[4]
                if correct:
                    await db.execute("UPDATE counting_stats SET guild_id = ?, user_id = ?, correct = ?, wrong = ?, "
                                     "highest = ?, last_counted= ?"
                                     "WHERE guild_id = ? AND user_id = ?",
                                     (guild_id, user_id, result[2] + 1, result[3], highest, last_counted, guild_id,
                                      user_id))
                    logging.info(f"[Counting] Updated stats entry for {guild_id} and {user_id}, set it to "
                                 f"{result[2] + 1}, {result[3]}, {highest}, {last_counted})")
                else:
                    await db.execute(f"UPDATE counting_stats SET guild_id = ?, user_id = ?, correct = ?, wrong = ?,"
                                     f"last_counted = ?"
                                     " WHERE guild_id = ? AND user_id = ?",
                                     (guild_id, user_id, result[2], result[3] + 1, last_counted, guild_id, user_id))
                    logging.info(f"[Counting] Updated stats entry for {guild_id} and {user_id}, set it to "
                                 f"{result[2]}, {result[3] + 1}, {highest}, {last_counted})")
                await db.commit()
                return


async def stats_delete_entry(guild_id: int, user_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting_stats WHERE guild_id='{guild_id}' AND user_id='{user_id}'") as \
                cursor:
            result = await cursor.fetchone()
            if result is None:
                return
            else:
                await db.execute(f"DELETE FROM counting_stats WHERE guild_id = '{guild_id}' AND user_id = '{user_id}'")
                await db.commit()
                return user_id


async def stats_check_entry(guild_id: int, user_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting_stats WHERE guild_id='{guild_id}' AND user_id='{user_id}'") as \
                cursor:
            result = await cursor.fetchone()
            return result


async def blocked_users_new_entry(guild_id: int, user_id: int, moderator_id: int, reason: str = "No reason provided."):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting_blocked_users WHERE guild_id='{guild_id}' "
                              f"AND user_id='{user_id}'") as cursor:
            result = await cursor.fetchone()
            if result is None:
                return
            else:
                await db.execute("INSERT INTO counting_blocked_users(guild_id, user_id, moderator_id, reason)"
                                 "VALUES (?, ?, ?, ?)",
                                 (guild_id, user_id, moderator_id, reason))
                await db.commit()
                logging.info(f"[Counting] {moderator_id} blocked {user_id} in {guild_id} for {reason}")
                return


async def blocked_users_check_entry(guild_id: int, user_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting_blocked_users WHERE guild_id='{guild_id}' "
                              f"AND user_id='{user_id}'") as cursor:
            result = await cursor.fetchone()
            return result


async def blocked_users_delete_entry(guild_id: int, user_id: int):
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(f"SELECT * FROM counting_blocked_users WHERE guild_id='{guild_id}' "
                              f"AND user_id='{user_id}'") as cursor:
            result = await cursor.fetchone()
            if result is None:
                return
            else:
                await db.execute(f"DELETE FROM counting_blocked_users WHERE guild_id = '{guild_id}'"
                                 f"AND user_id = '{user_id}'")
                await db.commit()
                return user_id
