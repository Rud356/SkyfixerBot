from typing import Optional

from discord import Member
from discord.ext.commands import Converter

from Skyfixer.extended_discord_classes import SkyfixerContext


class TextAfterFirstMention(Converter):
    """
    Gives text that goes after command and mention following the command.
    Here's example: s!command <@mentioned_user> text.
    This will give you `text`.

    Warning: this assumes that mention is going before text, but not somewhere else.
    """
    async def convert(self, ctx: SkyfixerContext, argument: Member) -> Optional[str]:
        message_text: str = ctx.message.content
        parts = message_text.split(" ", 2)

        if len(parts) == 3:
            return parts[2]

        else:
            return None
