from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Column, String, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from Skyfixer.config import skyfixer_config, validators
from Skyfixer.models.sqlalchemy_objects import Base


class Server(Base):
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    prefix = Column(String(3), default=skyfixer_config.default_prefix.value)

    announcements_channel_id = Column(BigInteger, autoincrement=False)
    moderation_channel_id = Column(BigInteger, autoincrement=False)
    welcome_channel_id = Column(BigInteger, autoincrement=False)

    __tablename__ = "servers"

    @classmethod
    async def get_or_create(cls, server_id: int, *, session: AsyncSession) -> Server:
        """
        Gets or creates discord server object.

        :param server_id: discord guild (server) id.
        :param session: sqlalchemy session.
        :return: record about discord server.
        """
        server_query = select(Server).filter_by(id=server_id)
        query_result = await session.execute(server_query)

        try:
            server: Server = query_result.scalar_one()

        except exc.NoResultFound:
            server = Server(id=server_id)
            session.add(server)
            await session.commit()

        return server

    @staticmethod
    async def get_prefix(server_id: str, *, session) -> str:
        """
        Returns prefix for this server.

        :param server_id: discord guild (server) id.
        :param session: sqlalchemy session.
        :return: discords server prefix.
        """
        server_query = select(Server.prefix).filter_by(id=server_id)
        query_result = await session.execute(server_query)

        prefix: str = query_result.one_or_none()
        return prefix or skyfixer_config.DEFAULT_PREFIX.value

    async def set_prefix(self, prefix: str, *, session: AsyncSession) -> None:
        """
        Sets prefix for this server.

        :param prefix: commands prefix.
        :param session: sqlalchemy session.
        :return: nothing.
        """
        is_valid, prefix = validators.validate_prefix(prefix)

        if not is_valid:
            raise ValueError("Invalid prefix")

        self.prefix = prefix
        await session.commit()

    async def set_announcements_channel(self, channel_id: Optional[int] = None, *, session: AsyncSession) -> None:
        """
        Sets an announcements channel where announcements from moderators/admins can be sent.

        :param channel_id: discord channel id.
        :param session: sqlalchemy session.
        :return: nothing.
        """
        self.announcements_channel_id = channel_id
        await session.commit()

    async def set_moderation_log_channel(self, channel_id: Optional[int] = None, *, session: AsyncSession) -> None:
        """
        Sets an moderation log channel where actions like warnings will be sent.

        :param channel_id: discord channel id.
        :param session: sqlalchemy session.
        :return: nothing.
        """
        self.moderation_channel_id = channel_id
        await session.commit()

    async def set_welcome_channel(self, channel_id: Optional[int] = None, *, session: AsyncSession) -> None:
        """
        Sets an welcome channel where greetings for new users will be sent.

        :param channel_id: discord channel id.
        :param session: sqlalchemy session.
        :return: nothing.
        """
        self.welcome_channel_id = channel_id
        await session.commit()
