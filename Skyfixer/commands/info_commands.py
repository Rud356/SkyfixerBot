from discord.ext import commands
from discord.ext.commands import Cog, command

from Skyfixer.extended_discord_classes import SkyfixerContext
from Skyfixer.models import ServerMember
from Skyfixer.skyfixer import skyfixer_bot


class InfoCommands(Cog):
    """Commands for checking users stats"""
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command()
    @commands.check(lambda ctx: not ctx.is_dm)
    async def level(self, ctx: SkyfixerContext):
        if len(ctx.message.mentions) > 0:
            server_member_user = ctx.message.mentions[0]
            server_member = ServerMember.get_or_create(server_member_user.id, ctx.guild.id)

        else:
            server_member_user = ctx.author
            server_member = ctx.db_server_member

        text = ctx.db_author.translate_phrase("users_level").safe_substitute(
            member_mention=server_member_user.mention, level=server_member.level
        )
        await ctx.send(text)

    @command()
    @commands.check(lambda ctx: not ctx.is_dm)
    async def exp(self, ctx: SkyfixerContext):
        if len(ctx.message.mentions) > 0:
            server_member_user = ctx.message.mentions[0]
            server_member = await ServerMember.get_or_create(
                server_member_user.id, ctx.guild.id, session=ctx.session
            )

        else:
            server_member_user = ctx.author
            server_member = ctx.db_server_member

        text = ctx.db_author.translate_phrase("users_exp").safe_substitute(
            member_mention=server_member_user.mention, level=server_member.exp
        )
        await ctx.send(text)
