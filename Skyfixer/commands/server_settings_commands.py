from discord.ext import commands
from discord.ext.commands import command

from Skyfixer.extended_discord_classes import SkyfixerCog, SkyfixerContext
from Skyfixer.skyfixer import skyfixer_bot
from Skyfixer.config import skyfixer_logs_config
from sqlalchemy.exc import IntegrityError


class ServerSettingsCommands(SkyfixerCog, name="Server settings_keys commands"):
    """
    Commands to change server settings_keys.
    """
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def set_prefix(self, ctx: SkyfixerContext, prefix: str):
        """
        Sets prefix for server
        Prefix must match regex: ^([a-zA-Z!\\-+=?|$#]){1,2}$
        """
        try:
            await ctx.db_server.set_prefix(prefix, session=ctx.session)
            msg = ctx.translate("updated_prefix").safe_substitute(new_prefix=prefix)

        except ValueError:
            msg = ctx.translate("invalid_prefix_set").safe_substitute()

        await ctx.send(msg)

    @set_prefix.error
    async def handle_set_prefix_errors(self, ctx: SkyfixerContext, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.TooManyArguments):
            msg = ctx.translate("no_prefix_provided").safe_substitute()
            await ctx.send(msg, delete_after=10)
            await ctx.message.delete(delay=5)

        else:
            await self.cog_command_error(ctx, error, ignore_error_handler=True)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def set_welcome_channel(self, ctx: SkyfixerContext):
        """
        Sets current channel as welcome channel
        Welcome channel will be used to greet new users
        """
        await ctx.db_server.set_welcome_channel(
            ctx.channel.id, session=ctx.session
        )
        msg = ctx.translate("new_welcome_channel_set").safe_substitute(
            ctx.channel.mention
        )
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def unset_welcome_channel(self, ctx: SkyfixerContext):
        """
        Unbinds current welcome channel
        """
        await ctx.db_server.set_welcome_channel(
            None, session=ctx.session
        )
        msg = ctx.translate("removed_welcome_channel").safe_substitute()
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def set_announcement_channel(self, ctx: SkyfixerContext):
        """
        Sets current channel as announcements
        Announcements channel will be used to send announcements via specific commands
        """
        await ctx.db_server.set_announcements_channel(
            ctx.channel.id, session=ctx.session
        )
        msg = ctx.translate("new_welcome_channel_set").safe_substitute(
            ctx.channel.mention
        )
        await (await ctx.send(msg)).delete(delay=10)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def unset_announcement_channel(self, ctx: SkyfixerContext):
        """
        Unbinds current announcement channel
        """
        await ctx.db_server.set_announcements_channel(
            None, session=ctx.session
        )
        msg = ctx.translate("removed_welcome_channel").safe_substitute()
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def set_moderation_log_channel(self, ctx: SkyfixerContext):
        """
        Sets current channel as moderation log
        Moderation log channel will be used to send messages about bans, kicks and other notifications
        """
        await ctx.db_server.set_moderation_log_channel(
            ctx.channel.id, session=ctx.session
        )
        msg = ctx.translate("new_moderation_log_channel_set").safe_substitute(
            ctx.channel.mention
        )
        await (await ctx.send(msg)).delete(delay=10)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def unset_moderation_log_channel(self, ctx: SkyfixerContext):
        """
        Unbinds current moderation log channel
        """
        await ctx.db_server.set_moderation_log_channel(
            None, session=ctx.session
        )
        msg = ctx.translate("removed_moderation_log_channel").safe_substitute()
        await ctx.send(msg, delete_after=5)
        await ctx.message.delete(delay=5)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def set_server_language(self, ctx: SkyfixerContext, language: str):
        """
        Sets new default language for server
        New language will be used in commands text, invoked by users
        (if language is forced to use in server) and in moderation logs.
        """
        try:
            await ctx.db_server.set_language(language, session=ctx.session)
            text = ctx.translate("new_language_set_successfully").safe_substitute(
                language=language
            )

        except (ValueError, IntegrityError):
            await ctx.session.rollback()
            text = ctx.translate("invalid_language").safe_substitute()

        await ctx.send(text)

    @set_server_language.error
    async def handle_set_language_errors(self, ctx: SkyfixerContext, error):
        if type(error) in {
            commands.TooManyArguments, commands.BadArgument,
            commands.MissingRequiredArgument
        }:
            msg = ctx.translate("no_language_provided").safe_substitute()
            await ctx.send(msg, delete_after=10)
            await ctx.message.delete(delay=5)

        else:
            skyfixer_logs_config.logger.exception(error)
            msg = ctx.translate("something_gone_wrong").safe_substitute()
            await ctx.send(msg)

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def set_force_language(self, ctx: SkyfixerContext, force_language: bool):
        """Sets if language for commands text should be same as server language."""
        ctx.db_server.settings.force_server_language = force_language
        await ctx.session.commit()

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def server_settings_list(self, ctx: SkyfixerContext):
        pass

    @command()
    @commands.check(commands.guild_only())
    @commands.check(commands.has_permissions(administrator=True))
    async def update_settings(self, ctx: SkyfixerContext, setting: str, value: bool):
        try:
            ctx.db_server.settings.update_setting(setting, value)

        except KeyError:
            pass