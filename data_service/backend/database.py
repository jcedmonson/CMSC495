from os import getenv
import logging
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from sqlalchemy.exc import SQLAlchemyError
from data_service.app_settings import Settings

logger = logging.getLogger("app.db")


@dataclass
class Database:
    engine: AsyncEngine = field(init=False)
    session: async_sessionmaker = field(init=False)
    settings: Settings = field(init=False)

    def __post_init__(self):
        self.settings = Settings()

        self.engine = create_async_engine(
            self.settings.dns,
            echo=True,
            connect_args={
                "server_settings": {
                    "application_name": self.settings.app_name
                }
            },
            pool_size=2, max_overflow=10
        )

        self.session = async_sessionmaker(self.engine,
                                          expire_on_commit=False,
                                          autoflush=False,
                                          autocommit=False,
                                          future=True)

    async def get_session(self) -> AsyncSession:
        try:
            yield self.session
        except SQLAlchemyError as error:
            logger.exception(error)
