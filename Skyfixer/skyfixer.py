import discord
from discord import Message
from discord.ext.commands import AutoShardedBot
from sqlalchemy.ext.asyncio import AsyncSession

from Skyfixer.config import skyfixer_config
from Skyfixer.extended_discord_classes import SkyfixerContext
from Skyfixer.models import Server, Session


class SkyfixerBot(AutoShardedBot):
    __version__ = "2.0.0"
    default_activity = discord.Activity(
        name="I'm listening to you my friend!~",
        type=discord.ActivityType.custom
    )

    @staticmethod
    async def command_prefix(message: Message):
        if message.guild is not None:
            session: AsyncSession = Session()
            prefix = await Server.get_prefix(message.guild.id, session=session)

            await session.close()

        else:
            prefix = skyfixer_config.DEFAULT_PREFIX.value

        return prefix

    async def get_context(self, message, *, cls=SkyfixerContext) -> SkyfixerContext:
        context: SkyfixerContext = await super(SkyfixerBot, self).get_context(message, cls=cls)
        await context.post_init()

        return context

    async def invoke(self, ctx: SkyfixerContext):
        await super().invoke(ctx)
        await ctx.session.close()


skyfixer_bot = SkyfixerBot(
    command_prefix=skyfixer_config.default_prefix.value,
    description="Skyfixer 2.0!", intents=discord.Intents.all()
)


@skyfixer_bot.event
async def on_ready():
    print(
        "Logged in as",
        f"Name: {skyfixer_bot.user.name}",
        f"DevID: {skyfixer_bot.user.id}",
        f"Discord.py {discord.__version__}",
        'Log start', sep='\n'
    )
    await skyfixer_bot.change_presence(activity=skyfixer_bot.default_activity)
