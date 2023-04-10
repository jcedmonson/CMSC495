import logging.config

from fastapi import FastAPI

from data_service.logging_config import LOGGING_CONFIG
from data_service.backend.main import routers
from data_service.backend.database import Database
from data_service.app_settings import Settings

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger("app")

settings = Settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.version
)
app.include_router(routers)


@app.on_event("startup")
def startup() -> None:
    app.db = Database()
    log.info("Database Initialized...")


@app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                log_level="info")
