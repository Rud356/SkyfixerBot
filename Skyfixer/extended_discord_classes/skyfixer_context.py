from typing import Optional

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
        # Since we can not modify the context in init - we should post-initialize additional stuff
        if self.is_dm:
            self.db_author = await User.get_or_create(self.author.id, session=self.session)  # noqa

        else:
            self.db_server_member = await ServerMember.get_or_create(
                self.author.id, self.guild.id, session=self.session
            )
            self.db_author = self.db_server_member.user  # noqa
            self.db_server = self.db_server_member.server
