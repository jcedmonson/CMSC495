import logging.config

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings import Settings
from models.base import Base
from backend.database import database, get_session
from models.user_account import UserAccount, UserCreate, UserLogin, UserAuthed

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
async def login(user: UserLogin,
                session: AsyncSession = Depends(get_session)) -> UserAuthed:
    try:
        result = await UserAccount.login_user(session, settings, user)
    except:
        raise

    return result


@auth_app.post("/user", status_code=201)
async def user_create(user: UserCreate,
                      session: AsyncSession = Depends(get_session)) -> UserAuthed:
    """Create a new user. If there is an error, a raise is set"""

    result = await UserAccount.create_user(session, settings, user)

    if isinstance(result, str):
        raise HTTPException(status_code=404, detail=result)

    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app", host="0.0.0.0", port=8888,
                log_level="debug", reload=True)
