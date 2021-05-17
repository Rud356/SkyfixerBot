from Skyfixer.extended_discord_classes import SkyfixerContext

from Skyfixer.skyfixer import skyfixer_bot


@skyfixer_bot.command()
async def ping(ctx: SkyfixerContext):
    """
    Responds with pong on your message!
    """
    text = ctx.db_author.translate_phrase("ping").safe_substitute()
    await ctx.reply("Pong!")


@skyfixer_bot.command()
async def hello_world(ctx: SkyfixerContext):
    text = ctx.db_author.translate_phrase("hello_world").safe_substitute()
    await ctx.send(text)
