import logging.config

from fastapi import FastAPI

from auth_app.backend.main import routers
from auth_app.app_settings import Settings
from auth_app.models.base import Base
from auth_app.backend.database import database

settings = Settings()
logging.config.dictConfig(settings.log_settings)
log = logging.getLogger("app")


auth_app = FastAPI(
    title=settings.app_name,
    version=settings.version
)
auth_app.include_router(routers)


@auth_app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        if settings.drop_tables:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    log.info("Database Initialized...")


@auth_app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app", host="0.0.0.0", port=8888,
                log_level="debug", reload=True)