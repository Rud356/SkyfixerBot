from discord.ext import commands

from Skyfixer.config import logger
from Skyfixer.extended_discord_classes import SkyfixerContext


@commands.Cog.listener()
async def on_command_error(ctx: SkyfixerContext, error, ignore_error_handler=False):
    if ctx.command is None:
        msg = ctx.db_author.translate_phrase("no_command_found").safe_substitute()
        await ctx.reply(msg)
        return

    if ctx.command.has_error_handler() and not ignore_error_handler:
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

    logger.exception(error)
    msg = ctx.db_author.translate_phrase("something_gone_wrong").safe_substitute()
    await ctx.send(msg)
