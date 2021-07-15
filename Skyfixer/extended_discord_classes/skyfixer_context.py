from typing import Optional

from string import Template
from discord import Message
from discord.ext.commands import Context
from sqlalchemy.ext.asyncio import AsyncSession

from Skyfixer.models import Server, ServerMember, Session, User


class SkyfixerContext(Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.message: Message
        self.db_author: User
        self.db_server: Optional[Server] = None
        self.db_server_member: Optional[ServerMember] = None

        self.session: AsyncSession = Session()
        self.is_dm: bool = getattr(self.guild, 'id', None) is None

    async def post_init(self):
        # Since we can not modify (cause async is needed) the context in init
        # we should post-initialize additional stuff
        if self.is_dm:
            self.db_author = await User.get_or_create(self.author.id, session=self.session)  # noqa

        else:
            self.db_server_member = await ServerMember.get_or_create(
                self.author.id, self.guild.id, session=self.session
            )
            self.db_author = self.db_server_member.user  # noqa
            self.db_server = self.db_server_member.server

    def translate(self, key: str) -> Template:
        # If we have fetched server and it forces some language - it will be used.
        if self.db_server and self.db_server.settings.force_server_language:
            return self.db_server.translate_phrase(key)

        else:
            return self.db_author.translate_phrase(key)
