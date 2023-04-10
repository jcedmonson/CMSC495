import logging.config

from fastapi import FastAPI

from data_service.logging_config import LOGGING_CONFIG
from data_service.backend.main import routers
from data_service.app_settings import Settings
from data_service.models.base import Base
from data_service.backend.database import database

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("app")

settings = Settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.version
)
app.include_router(routers)


@app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        if settings.drop_tables:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    log.info("Database Initialized...")


@app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                log_level="debug", reload=True)
