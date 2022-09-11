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

from typing import TypeVar, Callable
import disnake.ext.commands
from disnake.ext import commands
from disnake.ext.commands.context import AnyContext

T = TypeVar("T")


def checks_is_owner() -> Callable[[T], T]:
    async def predicate(ctx: AnyContext) -> bool:
        if not await ctx.bot.is_owner(ctx.author):
            raise disnake.ext.commands.NotOwner
        return True

    return commands.check(predicate)
