from discord.ext import commands
from discord.ext.commands import Cog, command

from Skyfixer.config import logger
from Skyfixer.extended_discord_classes import SkyfixerContext
from Skyfixer.models import ServerMember
from Skyfixer.skyfixer import skyfixer_bot
from .embeds import about_me_embed


class InfoCommands(Cog, name="Information commands"):
    """Commands for checking users stats"""
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: SkyfixerContext, error, ignore_error_handler=False):
        if ctx.command.has_error_handler() and not ignore_error_handler:
            return

        if isinstance(error, commands.NoPrivateMessage):
            msg = ctx.db_author.translate_phrase("only_for_servers").safe_substitute()
            await ctx.send(msg)

        if isinstance(error, commands.CheckAnyFailure) or isinstance(error, commands.NotOwner):
            msg = ctx.db_author.translate_phrase("no_permissions").safe_substitute()
            await ctx.send(msg)

        logger.exception(error)
        msg = ctx.db_author.translate_phrase("something_gone_wrong").safe_substitute()
        await ctx.send(msg)

    @command()
    @commands.check(commands.guild_only())
    async def level(self, ctx: SkyfixerContext):
        """Shows your level on this server"""
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
    @commands.check(commands.guild_only())
    async def exp(self, ctx: SkyfixerContext):
        """Shows your experience, earned in this specific server"""
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

    @command()
    async def about_skyfixer(self, ctx: SkyfixerContext):
        """Sends information about me, your favourite girl!"""
        embed = about_me_embed.generate_about_me(
            self.bot, ctx.db_author.language
        )

        await ctx.send(embed=embed)
