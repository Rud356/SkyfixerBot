from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Cog

from Skyfixer.config import logger

if TYPE_CHECKING:
    from .skyfixer_context import SkyfixerContext


class SkyfixerCog(Cog):
    async def cog_command_error(self, ctx: SkyfixerContext, error, ignore_error_handler=False):
        if hasattr(ctx.command, "error_handler") and not ignore_error_handler:
            return

        if isinstance(error, commands.NoPrivateMessage):
            msg = ctx.db_author.translate_phrase("only_for_servers").safe_substitute()
            await ctx.send(msg)
            return

        if (
                isinstance(error, commands.MissingPermissions) or
                isinstance(error, commands.NotOwner) or
                isinstance(error, commands.BotMissingPermissions)
        ):
            msg = ctx.db_author.translate_phrase("no_permissions").safe_substitute()
            await ctx.send(msg)
            return

        if not isinstance(error, commands.CommandNotFound):
            logger.exception(error)
            msg = ctx.db_author.translate_phrase("something_gone_wrong").safe_substitute()
            await ctx.send(msg)
