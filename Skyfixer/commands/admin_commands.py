from typing import Optional

from discord import Member
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
    async def ban(self, ctx: SkyfixerContext, mentioned_user: Member, reason: Optional[TextAfterFirstMention] = None):
        user_who_bans: Member = ctx.message.author
        user_who_will_be_banned: Member = mentioned_user
        has_higher_role = (user_who_bans.top_role > user_who_will_be_banned.top_role)

        if has_higher_role:
            if reason is None:
                reason = ctx.db_server.translate_phrase("default_ban_reason")

            else:
                reason = ctx.db_server.translate_phrase("ban_reason")

            await user_who_will_be_banned.ban(reason=reason.safe_substitute(
                user_who_bans=user_who_bans.mention,
                user_who_will_be_banned=user_who_will_be_banned,
                reason=reason
            ))
