from __future__ import annotations

from functools import lru_cache
from math import ceil, sqrt
from random import randint

from sqlalchemy import Column, ForeignKey, BigInteger, Integer, PrimaryKeyConstraint, and_, exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from Skyfixer.models.sqlalchemy_objects import Base
from .server import Server
from .user import User


class ServerMember(Base):
    member_id = Column(ForeignKey("users.id"), index=True, nullable=False)
    server_id = Column(ForeignKey("servers.id"), index=True, nullable=False)
    exp = Column(BigInteger, default=0)
    level = Column(Integer, default=1)
    ban_counter = Column(Integer, default=0)
    kick_counter = Column(Integer, default=0)

    user: User = relationship(User, lazy="joined", uselist=False)
    server: Server = relationship(Server, lazy="joined", uselist=False)

    __tablename__ = "servermembers"
    __table_args__ = (
        PrimaryKeyConstraint('member_id', 'server_id'),
        {},
    )

    @classmethod
    async def get_or_create(cls, user_id: int, server_id: int, *, session: AsyncSession) -> ServerMember:
        """
        Gets or creates server member.

        :param user_id: member id.
        :param server_id: server id where we look up user.
        :param session: sqlalchemy session.
        :return: server member instance.
        """
        server_member_query = select(ServerMember).filter(
            and_(
                ServerMember.member_id == user_id,
                ServerMember.server_id == server_id
            )
        )
        query_result = await session.execute(server_member_query)

        try:
            server_member = query_result.scalar_one()

        except exc.NoResultFound:
            user = await User.get_or_create(user_id, session=session)
            server = await Server.get_or_create(server_id, session=session)
            server_member = ServerMember(user=user, server=server)  # noqa: this should work ewfweeing to the docs
            session.add(server_member)

        return server_member

    async def add_exp_amount(self, amount: int, *, session: AsyncSession) -> None:
        """
        Gives some exp to user.

        :param amount: how much exp to give this user.
        :param session: sqlalchemy session.
        :return: nothing.
        """
        self.exp += amount
        await session.commit()

    async def increase_exp(self, *, session: AsyncSession) -> None:
        """
        Increases exp for message.

        :param session: sqlalchemy session.
        :return: nothing
        """
        exp_amount = randint(15, 25) * ceil(sqrt(self.level))

        if self.exp + exp_amount >= self.next_level_requirement(self.level):
            self.level += 1

        await session.commit()

    async def ban(self, *, session: AsyncSession) -> None:
        """
        Increases bans count for this user.

        :param session: sqlalchemy session.
        :return: nothing
        """
        self.ban_counter += 1
        await session.commit()

    async def kick(self, *, session: AsyncSession) -> None:
        """
        Increases kick count for user.

        :param session: sqlalchemy session.
        :return: nothing
        """
        self.kick_counter += 1
        await session.commit()

    @staticmethod
    @lru_cache(None)
    def next_level_requirement(level: int) -> int:
        """
        Calculates how much exp is required for next level

        :param level: for what level we calculate exp for.
        :return: amount of exp required to achieve this level.
        """
        return round(
            100 * (round(sqrt(level + 1), 2) + level)
        )
