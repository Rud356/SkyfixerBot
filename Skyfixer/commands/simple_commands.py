from datetime import datetime
from random import choice, randint

from discord.ext.commands import Cog, command

from Skyfixer.extended_discord_classes import SkyfixerContext
from Skyfixer.skyfixer import skyfixer_bot


class SimpleCommands(Cog, name="Simple commands"):
    """
    Bunch of simple commands.
    """
    def __init__(self, bot=skyfixer_bot):
        self.bot = bot

    @command()
    async def ping(self, ctx: SkyfixerContext):
        """
        Responds with pong on your message!
        """
        text = ctx.db_author.translate_phrase("ping").safe_substitute()
        await ctx.reply(text)

    @command(aliases=("helloWorld", ))
    async def hello_world(self, ctx: SkyfixerContext):
        """
        Sends hello world in chat.
        """
        text = ctx.db_author.translate_phrase("hello_world").safe_substitute()
        await ctx.send(text)

    @command()
    async def coin(self, ctx: SkyfixerContext):
        """Flips a coin for you."""
        side = choice(("heads", "tails"))
        translate_side = ctx.db_author.translate_phrase(f"coin_side_{side}").safe_substitute()
        text = ctx.db_author.translate_phrase("coin_flip").safe_substitute(side=translate_side)
        await ctx.send(text)

    @command()
    async def pick(self, ctx: SkyfixerContext):
        """Picks one option from many, separated by ; (semi-colon)"""
        cmd_len = len(ctx.prefix) + len(ctx.invoked_with)
        options = ctx.message.content[cmd_len:].split("; ")

        if len(options) < 2:
            text = ctx.db_author.translate_phrase(f"not_enough_args").safe_substitute(num=2)
            await ctx.send(text)
            return

        text = ctx.db_author.translate_phrase(f"bots_choice").safe_substitute(words=choice(options).strip())
        await ctx.send(text)

    @command(aliases=("utcnow", "now"))
    async def time(self, ctx: SkyfixerContext):
        """Tells what time is in 0 timezone.
        Format: %m/%d/%Y # %H:%M.%S
        """
        text = ctx.db_author.translate_phrase("current_time").safe_substitute(
            datetime=datetime.utcnow().strftime("%m/%d/%Y # %H:%M.%S")
        )
        await ctx.send(text)

    @command()
    async def dice(self, ctx: SkyfixerContext):
        """Rolls a dice and gives you number on it!"""
        text = ctx.db_author.translate_phrase("roll_the_dice").safe_substitute(num=randint(1, 6))
        await ctx.send(text)

    @command()
    async def ship(self, ctx: SkyfixerContext):
        """Ships two mentioned users or two words sequence separated by +"""
        cmd_len = len(ctx.prefix) + len(ctx.invoked_with)
        clear_content = ctx.message.content[cmd_len:]

        if len(ctx.message.mentions) >= 2:
            shipping, shipping_with, *_ = ctx.message.mentions
            shipping, shipping_with = shipping.mention, shipping_with.mention

        elif '+' in clear_content:
            shipping, shipping_with = [obj.strip() for obj in clear_content.split('+')[:2]]
            shipping = shipping.capitalize()

        else:
            text = ctx.db_author.translate_phrase(f"not_enough_args").safe_substitute(num=2)
            await ctx.send(text)
            return

        percent = randint(10, 1002) / 10
        text = ctx.db_author.translate_phrase("shipping").safe_substitute(
            shipping=shipping, shipping_with=shipping_with, percent=percent
        )
        await ctx.send(text)
