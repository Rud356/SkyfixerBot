from __future__ import annotations

from secrets import token_urlsafe
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, String, UniqueConstraint, func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from Skyfixer.models.sqlalchemy_objects import Base

if TYPE_CHECKING:
    from .server import Server


class ServerGreetings(Base):
    # token_urlsafe encodes bytes as base64 and so 8 characters will be generated from 6 bytes
    short_code = Column(String(8), default=lambda: token_urlsafe(6))
    server_id = Column(ForeignKey("servers.id"), index=True)

    phrase = Column(String(2000))

    __tablename__ = "greetings_phrases"
    __table_args__ = (
        UniqueConstraint('server_id', 'phrase'),
        PrimaryKeyConstraint('short_code', 'server_id'),
        {},
    )

    @classmethod
    async def get_random_greeting(cls, server_id: int, *, session: AsyncSession) -> Optional[ServerGreetings]:
        random_phrase_query = select(ServerGreetings.phrase).filter(ServerGreetings.server_id == server_id) \
            .order_by(func.random()).limit(1)
        random_phrase_result = await session.execute(random_phrase_query)
        random_phrase = random_phrase_result.scalar()

        return random_phrase

    @classmethod
    async def add_phrase(cls, server: Server, phrase: str, *, session: AsyncSession) -> ServerGreetings:
        phrases_count_query = select(ServerGreetings.id).filter(ServerGreetings.server_id == server.id).count()
        phrases_count = (await session.execute(phrases_count_query)).scalar()

        if phrases_count >= server.greetings_limit:
            raise ValueError("Already filled all slots for greetings")

        new_greeting = cls(server_id=server.id, phrase=phrase)
        session.add(new_greeting)
        await session.commit()

        return new_greeting

    @classmethod
    async def get_phrase(cls, server_id: int, short_code: str, *, session: AsyncSession) -> ServerGreetings:
        phrase_query = select(ServerGreetings).filter(
            and_(
                ServerGreetings.server_id == server_id,
                ServerGreetings.short_code == short_code
            )
        )
        phrase = (await session.execute(phrase_query)).scalar_one()
        return phrase
