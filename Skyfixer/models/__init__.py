from functools import wraps

from sqlalchemy.exc import SQLAlchemyError

from Skyfixer.config import logger
from Skyfixer.models.sqlalchemy_objects import Session, Base
from Skyfixer.models.server import Server
from Skyfixer.models.server_member import ServerMember
from Skyfixer.models.user import User
from Skyfixer.models.server_greetings import ServerGreetings


def async_session(f):
    @wraps(f)
    async def grab_session(*args, **kwargs):
        async with Session() as session:
            try:
                return await f(*args, **kwargs, session=session)

            except SQLAlchemyError as err:
                await session.rollback()
                logger.exception(err)

    return grab_session
