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

import sqlite3

import sqlite3

connection = sqlite3.connect("database/database.db")
cursor = connection.cursor()

count_info_headers = ['guild_id', 'channel_id', 'count', 'last_user', 'fail_message', 'greedy_message']


def new_counting_entry(guild_id,
                       channel_id,
                       count=str(0),
                       last_user=str(None),
                       fail_message=str("{{{user}}} typed the wrong number"),
                       greedy_message=str("{{{user}}} was too greedy")):
    temp1 = [
        str(guild_id),
        str(channel_id),
        str(count),
        str(last_user),
        str(fail_message),
        str(greedy_message)]

    cursor.execute("INSERT INTO counting %s VALUES %s" % (tuple(count_info_headers), tuple(temp1)))
    connection.commit()
