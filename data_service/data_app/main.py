import logging.config

from fastapi import FastAPI

from endpoints.routers import routers
from endpoints.database import database

from app_settings import get_settings
from models.base import Base

logging.config.dictConfig(get_settings().log_settings)
log = logging.getLogger("app")

data_app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().version
)
data_app.include_router(routers)


@data_app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        if get_settings().drop_tables:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    log.info("Database Initialized...")


@data_app.post("/sync_user")
async def sync_new_user() -> None:
    return None



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:data_app", host="0.0.0.0", port=8080,
                log_level="debug", reload=True)
