from __future__ import annotations

from datetime import datetime
from string import Template

from sqlalchemy import BigInteger, Boolean, Column, Date, String, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from Skyfixer.localisation import translator
from Skyfixer.models.sqlalchemy_objects import Base


class User(Base):
    id = Column(BigInteger, primary_key=True)
    language = Column(String(20), default='en')

    coins = Column(BigInteger, default=1000)
    birthday = Column(Date, nullable=True)

    hide_age = Column(Boolean, default=True)
    hide_birthday = Column(Boolean, default=True)

    __tablename__ = "users"

    @classmethod
    async def get_or_create(cls, user_id: int, *, session: AsyncSession) -> User:
        """
        Gives or creates an discord users record.

        :param user_id: discord user id.
        :param session: sqlalchemy session.
        :return: instance of info about user.
        """
        user_query = select(cls).filter_by(id=user_id)
        query_result = await session.execute(user_query)

        try:
            user = query_result.scalar_one()

        except exc.NoResultFound:
            user = User(id=user_id)
            session.add(user)
            await session.commit()

        return user

    @property
    def age(self) -> int:
        """
        Gives age of user.

        :return: users age.
        """
        return (datetime.utcnow().date() - self.birthday).days // 365

    @property
    def display_birthday(self) -> str:
        """
        Shows a birthday date and hiding parts of it or not telling at all, depending on settings.

        :return: formatted birthday date.
        """
        if self.hide_birthday or self.birthday is None:
            raise PermissionError("Birthday is hidden")

        if self.hide_age:
            return self.birthday.strftime("%d/%m (day, month)")

        else:
            return self.birthday.strftime("%d/%m/%Y (day, month, year)")

    async def change_hiding_age(self, *, session: AsyncSession) -> None:
        self.hide_age = not self.hide_age
        await session.commit()

    async def change_hiding_birthday(self, *, session: AsyncSession) -> None:
        self.hide_birthday = not self.hide_birthday
        await session.commit()

    async def set_birthday(self, birthday: str, *, session: AsyncSession) -> None:
        birthday_date = datetime.strptime(birthday, "%d.%m.%Y").date()

        if birthday_date.month == 5 and birthday_date.day > 28:
            birthday_date = datetime(birthday_date.year, birthday_date.month, 28)

        if birthday_date > datetime.utcnow().date():
            raise self.exc.NoTimeTravellersAllowed("No time travellers allowed!")

        self.birthday = birthday_date
        await session.commit()

    async def add_coins_amount(self, amount: int, *, session: AsyncSession) -> None:
        if self.coins < amount:
            raise ValueError("Insufficient coins amount on account")

        self.coins += amount
        await session.commit()

    async def transfer_coins(self, amount: int, to_user: User, *, session: AsyncSession) -> None:
        if self.coins < amount or amount < 0:
            raise ValueError("Insufficient coins amount on account")

        self.coins -= amount
        to_user.coins += amount
        await session.commit()

    async def set_language(self, new_language: str, *, session: AsyncSession) -> None:
        if new_language not in translator.languages:
            raise ValueError("Invalid language")

        self.language = new_language
        await session.commit()

    def translate_phrase(self, key: str) -> Template:
        return translator.translate(key, self.language)

    class exc:
        class NoTimeTravellersAllowed(Exception):
            pass
