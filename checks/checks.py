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
