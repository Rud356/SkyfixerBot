from discord.ext import commands
from discord.ext.commands import command

from Skyfixer.extended_discord_classes import SkyfixerCog, SkyfixerContext
from Skyfixer.skyfixer import skyfixer_bot


class ServerSettingsCommands(SkyfixerCog, name="Server settings commands"):
    """
    Commands to change server settings.
    """
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def set_prefix(self, ctx: SkyfixerContext, prefix: str):
        """
        Sets prefix for server
        Prefix must match regex: ^([a-zA-Z!\\-+=?|$#]){1,2}$
        """
        try:
            await ctx.db_server.set_prefix(prefix, session=ctx.session)
            msg = ctx.db_author.translate_phrase("updated_prefix").safe_substitute(new_prefix=prefix)

        except ValueError:
            msg = ctx.db_author.translate_phrase("invalid_prefix_set").safe_substitute()

        await ctx.send(msg)

    @set_prefix.error
    async def handle_set_prefix_errors(self, ctx: SkyfixerContext, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.TooManyArguments):
            msg = ctx.db_author.translate_phrase("no_prefix_provided").safe_substitute()
            await ctx.send(msg, delete_after=10)
            await ctx.message.delete(delay=5)

        else:
            await self.cog_command_error(ctx, error, ignore_error_handler=True)

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def set_welcome_channel(self, ctx: SkyfixerContext):
        """
        Sets current channel as welcome channel
        Welcome channel will be used to greet new users
        """
        await ctx.db_server.set_welcome_channel(
            ctx.channel.id, session=ctx.session
        )
        msg = ctx.db_author.translate_phrase("new_welcome_channel_set").safe_substitute(
            ctx.channel.mention
        )
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def unset_welcome_channel(self, ctx: SkyfixerContext):
        """
        Stops sending messages to current welcome channel
        """
        await ctx.db_server.set_welcome_channel(
            None, session=ctx.session
        )
        msg = ctx.db_author.translate_phrase("removed_welcome_channel").safe_substitute()
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def set_announcement_channel(self, ctx: SkyfixerContext):
        """
        Sets current channel as announcements
        Announcements channel will be used to send announcements via specific commands
        """
        await ctx.db_server.set_announcements_channel(
            ctx.channel.id, session=ctx.session
        )
        msg = ctx.db_author.translate_phrase("new_welcome_channel_set").safe_substitute(
            ctx.channel.mention
        )
        await (await ctx.send(msg)).delete(delay=10)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def unset_announcement_channel(self, ctx: SkyfixerContext):
        """
        Stops sending messages to current announcement channel
        """
        await ctx.db_server.set_announcements_channel(
            None, session=ctx.session
        )
        msg = ctx.db_author.translate_phrase("removed_welcome_channel").safe_substitute()
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def set_moderation_log_channel(self, ctx: SkyfixerContext):
        """
        Sets current channel as moderation log
        Moderation log channel will be used to send messages about bans, kicks and other notifications
        """
        await ctx.db_server.set_moderation_log_channel(
            ctx.channel.id, session=ctx.session
        )
        msg = ctx.db_author.translate_phrase("new_moderation_log_channel_set").safe_substitute(
            ctx.channel.mention
        )
        await (await ctx.send(msg)).delete(delay=10)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.is_owner()
    )
    async def unset_moderation_log_channel(self, ctx: SkyfixerContext):
        """
        Stops sending messages to current moderation log channel
        """
        await ctx.db_server.set_moderation_log_channel(
            None, session=ctx.session
        )
        msg = ctx.db_author.translate_phrase("removed_moderation_log_channel").safe_substitute()
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)
