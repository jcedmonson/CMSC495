import logging.config

from fastapi import FastAPI

from data_app.logging_config import LOGGING_CONFIG
from data_app.backend.main import routers
from data_app.app_settings import Settings
from data_app.models.base import Base
from data_app.backend.database import database

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("app")

settings = Settings()


data_app = FastAPI(
    title=settings.app_name,
    version=settings.version
)
data_app.include_router(routers)


@data_app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        if settings.drop_tables:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    log.info("Database Initialized...")


@data_app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:data_app", host="0.0.0.0", port=8080,
                log_level="debug", reload=True)
