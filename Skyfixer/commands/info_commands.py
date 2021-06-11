from discord.ext import commands
from discord.ext.commands import Cog, command

from Skyfixer.extended_discord_classes import SkyfixerContext
from Skyfixer.models import ServerMember
from Skyfixer.skyfixer import skyfixer_bot
from Skyfixer.extended_discord_classes import SkyfixerCog
from .embeds import about_skyfixer, user_pm_info, about_user_info


class InfoCommands(SkyfixerCog, name="Information commands"):
    """Commands for checking users stats"""
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command()
    @commands.guild_only()
    async def level(self, ctx: SkyfixerContext):
        """Shows your level on this server"""
        if len(ctx.message.mentions) > 0:
            server_member_user = ctx.message.mentions[0]
            server_member = await ServerMember.get_or_create(
                server_member_user.id, ctx.guild.id, session=ctx.session
            )

        else:
            server_member_user = ctx.author
            server_member = ctx.db_server_member

        text = ctx.db_author.translate_phrase("users_level").safe_substitute(
            member_mention=server_member_user.mention, level=server_member.level
        )
        await ctx.send(text)

    @command()
    @commands.guild_only()
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
    async def about_user(self, ctx: SkyfixerContext):
        if ctx.is_dm:
            await ctx.send(embed=user_pm_info.user_pm_info(ctx.author, ctx.db_author))

        elif ctx.guild:
            if len(ctx.message.mentions):
                about_whom = ctx.message.mentions[0]
                server_member = await ServerMember.get_or_create(
                    user_id=about_whom.id, server_id=ctx.guild.id, session=ctx.session
                )

            else:
                about_whom = ctx.author
                server_member = ctx.db_server_member

            about_user_embed = about_user_info.user_server_info(
                about_whom, server_member.user, ctx.guild, server_member,
                language=ctx.db_author.language
            )
            await ctx.send(embed=about_user_embed)

        else:
            await ctx.send(
                ctx.db_author.translate_phrase("only_for_servers_and_dms").safe_substitute()
            )

    @command()
    async def about_skyfixer(self, ctx: SkyfixerContext):
        """Sends information about me, your favourite girl!"""
        embed = about_skyfixer.generate_about_me(
            self.bot, ctx.db_author.language
        )

        await ctx.send(embed=embed)
