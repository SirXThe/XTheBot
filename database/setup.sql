/*
 * XTheBot
 * Copyright (C) 2022  XThe
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

CREATE TABLE IF NOT EXISTS `counting` (
`guild_id` int NOT NULL,
`channel_id` int NOT NULL,
`mode` text NOT NULL,
`count` int NOT NULL,
`last_user` int NOT NULL,
`last_counted` text NOT NULL,
`resets` int NOT NULL,
`record` int NOT NULL,
`record_user` int NOT NULL,
`record_time` text NOT NULL
);
CREATE TABLE IF NOT EXISTS `stats` (
`guild_id` int NOT NULL,
`user_id`  int NOT NULL,
`correct`  int NOT NULL,
`wrong`    int NOT NULL,
`highest`  int NOT NULL,
`last_counted`  text NOT NULL
);
