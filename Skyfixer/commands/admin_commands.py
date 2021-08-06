from typing import Optional

from discord import Member, Guild, TextChannel
from discord.ext import commands
from discord.ext.commands import command

from Skyfixer.extended_discord_classes import SkyfixerCog, SkyfixerContext
from Skyfixer.models import ServerMember
from Skyfixer.skyfixer import skyfixer_bot
from .commands_utils import TextAfterFirstMention


class AdminCommands(SkyfixerCog, name="Admin commands"):
    """Commands for checking users stats"""
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command(require_var_positional=True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx: SkyfixerContext, mentioned_user: Member,
        reason: Optional[TextAfterFirstMention] = None
    ):
        user_who_bans: Member = ctx.message.author
        user_who_will_be_banned: Member = mentioned_user
        has_higher_role = (user_who_bans.top_role > user_who_will_be_banned.top_role)

        if has_higher_role:
            if reason is None:
                reason = ctx.db_server.translate_phrase("default_ban_reason")

            else:
                reason = ctx.db_server.translate_phrase("ban_reason")

            reason = reason.safe_substitute(
                user_who_bans=user_who_bans.mention,
                user_who_will_be_banned=user_who_will_be_banned,
                reason=reason
            )
            await user_who_will_be_banned.ban(reason=reason)
            await ctx.reply(
                ctx.translate("ban_success").safe_substitute(
                    user_to_ban=user_who_will_be_banned.mention
                )
            )

            if ctx.db_server.moderation_channel_id is not None:
                server: Guild = ctx.guild
                mod_channel: TextChannel = server.get_channel(ctx.db_server.moderation_channel_id)

                if mod_channel is None:
                    # Unbinding channel since it doesn't exists
                    await ctx.db_server.set_moderation_log_channel(
                        ctx.db_server.moderation_channel_id, session=ctx.session
                    )
                    return

                await mod_channel.send(reason)

        else:
            await ctx.reply(
                ctx.translate("user_tries_to_ban_someone_higher").safe_substitute()
            )

    @ban.error
    async def handle_ban_error(self, ctx: SkyfixerContext, error):
        if type(error) in {commands.BadArgument, commands.MissingRequiredArgument}:
            await ctx.reply(ctx.translate("no_user_to_ban_mentioned").safe_substitute())

        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(ctx.translate("user_missing_ban_permission").safe_substitute())

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(ctx.translate("bot_missing_bot_permission").safe_substitute())

        else:
            await self.cog_command_error(ctx, error, ignore_error_handler=True)

    @command(require_var_positional=True)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, ctx: SkyfixerContext, mentioned_user: Member,
        reason: Optional[TextAfterFirstMention] = None
    ):
        user_who_kicks: Member = ctx.message.author
        user_who_will_be_kicked: Member = mentioned_user
        user_who_kicks_is_owner = ctx.message.author == ctx.guild.owner
        has_higher_role = (user_who_kicks.top_role > user_who_will_be_kicked.top_role)

        if has_higher_role or user_who_kicks_is_owner:
            if reason is None:
                reason = ctx.db_server.translate_phrase("default_kick_reason")

            else:
                reason = ctx.db_server.translate_phrase("kick_reason")

            reason = reason.safe_substitute(
                user_who_kicks=user_who_kicks.mention,
                user_who_will_be_kicked=user_who_will_be_kicked,
                reason=reason
            )
            await user_who_will_be_kicked.kick(reason=reason)

            await ctx.reply(
                ctx.translate("kick_success").safe_substitute(
                    user_to_kick=user_who_will_be_kicked.mention
                )
            )

            if ctx.db_server.moderation_channel_id is not None:
                server: Guild = ctx.guild
                mod_channel: TextChannel = server.get_channel(ctx.db_server.moderation_channel_id)

                if mod_channel is None:
                    # Unbinding channel since it doesn't exists
                    await ctx.db_server.set_moderation_log_channel(
                        ctx.db_server.moderation_channel_id, session=ctx.session
                    )
                    return

                await mod_channel.send(reason)

        else:
            await ctx.reply(ctx.translate("user_tries_to_kick_someone_higher").safe_substitute())

    @kick.error
    async def handle_ban_error(self, ctx: SkyfixerContext, error):
        if type(error) in {commands.BadArgument, commands.MissingRequiredArgument}:
            await ctx.reply(ctx.translate("no_user_to_kick_mentioned").safe_substitute())

        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply(ctx.translate("user_missing_kick_permission").safe_substitute())

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.reply(ctx.translate("bot_missing_kick_permission").safe_substitute())

        else:
            await self.cog_command_error(ctx, error, ignore_error_handler=True)
