import logging.config

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings import Settings
from models.base import Base
from backend.database import database, get_session
from models.user_account import UserAccount, UserCreate, UserLogin

settings = Settings()

logging.config.dictConfig(settings.log_settings)
log = logging.getLogger("app")

auth_app = FastAPI(
    title=settings.app_name,
    version=settings.version
)


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


@auth_app.post("/login")
async def login(data: UserLogin,
                session: AsyncSession = Depends(get_session)) -> None:
    result = await UserAccount.login_user(session,
                                          data.user_name,
                                          data.password)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")


@auth_app.post("/user")
async def login(data: UserCreate,
                session: AsyncSession = Depends(get_session)) -> None:

    result = await UserAccount.create_user(session, data)

    if isinstance(result, str):
        raise HTTPException(status_code=404, detail=result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app", host="0.0.0.0", port=8888,
                log_level="debug", reload=True)
