"""
NOTES:

# Sessions are the usual way to interact with the database. They will fetch a
# connection when it is needed making it efficient. THe usual way
# to interact with it is with:

# with Session(engine) as session:
#     session.begin()
#     try:
#         session.add(some_object)
#         session.add(some_other_object)
#     except:
#         session.rollback()
#         raise
#     else:
#         session.commit()

# Just like with connection you can also use the `begin` to wrap
# these calls into one
# with Session(engine) as session, session.begin():
#     session.add(some_object)
#     session.add(some_other_object)

# With a session maker, we can make a session factory so that we don't have
# to keep specifying the engine and use it as a way to make the same config
# session. This makes the code a lot smaller with"

# with Session.begin() as session:
#     session.add(some_object)
#     session.add(some_other_object)

# it is typical for Engine and SessionMaker result be module level objects
# so that can be used globally by any thread (thread safe)

# Represent the metadata from ORM mapped class
"""
from os import getenv
import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

db_url = f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('HOST')}/{getenv('POSTGRES_DB')}"

async_engine = create_async_engine(
    db_url,
    echo=True,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield async_session
    except SQLAlchemyError as error:
        logger.exception(error)
