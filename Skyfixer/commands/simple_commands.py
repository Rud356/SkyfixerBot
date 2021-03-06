from datetime import datetime
from random import choice, randint

from discord import Message
from discord.ext.commands import command

from Skyfixer.extended_discord_classes import SkyfixerCog, SkyfixerContext
from Skyfixer.skyfixer import skyfixer_bot


class SimpleCommands(SkyfixerCog, name="Simple commands"):
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
        text = ctx.translate("ping").safe_substitute()
        await ctx.reply(text)

    @command(aliases=("helloWorld", ))
    async def hello_world(self, ctx: SkyfixerContext):
        """
        Sends hello world in chat.
        """
        text = ctx.translate("hello_world").safe_substitute()
        await ctx.send(text)

    @command()
    async def coin(self, ctx: SkyfixerContext):
        """Flips a coin for you"""
        side = choice(("heads", "tails"))
        translate_side = ctx.translate(f"coin_side_{side}").safe_substitute()
        text = ctx.translate("coin_flip").safe_substitute(side=translate_side)
        await ctx.send(text)

    @command()
    async def pick(self, ctx: SkyfixerContext):
        """Picks one option from many, separated by ; (semi-colon)"""
        cmd_len = len(ctx.prefix) + len(ctx.invoked_with)
        options = ctx.message.content[cmd_len:].split(";")

        if len(options) < 2:
            text = ctx.translate(f"not_enough_args").safe_substitute(num=2)
            await ctx.send(text)
            return

        text = ctx.translate(f"bots_choice").safe_substitute(words=choice(options).strip())
        await ctx.send(text)

    @command(aliases=("utcnow", "now"))
    async def time(self, ctx: SkyfixerContext):
        """Tells what time is in 0 timezone
        Format: %m/%d/%Y # %H:%M.%S
        """
        text = ctx.translate("current_time").safe_substitute(
            datetime=datetime.utcnow().strftime("%m/%d/%Y # %H:%M.%S")
        )
        await ctx.send(text)

    @command()
    async def dice(self, ctx: SkyfixerContext):
        """Rolls a dice and gives you number on it!"""
        text = ctx.translate("roll_the_dice").safe_substitute(num=randint(1, 6))
        await ctx.send(text)

    @command()
    async def ship(self, ctx: SkyfixerContext):
        """
        Ships two things (see full help)
        Mentioned users or two words sequence separated by + will be shipped
        """
        cmd_len = len(ctx.prefix) + len(ctx.invoked_with)
        clear_content = ctx.message.content[cmd_len:]

        if len(ctx.message.mentions) >= 2:
            shipping, shipping_with, *_ = ctx.message.mentions
            shipping, shipping_with = shipping.mention, shipping_with.mention

        elif '+' in clear_content:
            shipping, shipping_with = [obj.strip() for obj in clear_content.split('+')[:2]]
            shipping = shipping.capitalize()

        else:
            text = ctx.translate(f"not_enough_args").safe_substitute(num=2)
            await ctx.send(text)
            return

        percent = randint(10, 1002) / 10
        text = ctx.translate("shipping").safe_substitute(
            shipping=shipping, shipping_with=shipping_with, percent=percent
        )
        await ctx.send(text)

    @command(aliases=["reverse", "minecraft_enchantment_table"])
    async def reverse_text(self, ctx: SkyfixerContext):
        """Reverses given text after command or from reply"""
        message: Message = ctx.message

        if message.reference is not None:
            referenced_message = await ctx.fetch_message(message.reference.message_id)
            await referenced_message.reply(content=referenced_message.clean_content[::-1])

        else:
            message_text: str = message.clean_content  # noqa: this returns
            command_text, _, text = message_text.partition(' ')

            if not text:
                await message.reply(ctx.translate("no_text_to_reverse").safe_substitute())
                return

            await message.reply(content=text[::-1])
