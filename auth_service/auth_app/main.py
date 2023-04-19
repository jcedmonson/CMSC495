import logging.config
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from backend.database import database, get_session
from models.user_account import UserAccount, UserCreate, UserLogin, UserAuthed
from app_settings import Settings, oauth2_scheme
import models.jwt_token_handler as jwt


@lru_cache()
def get_settings():
    """Settings cache"""
    return Settings()


logging.config.dictConfig(get_settings().log_settings)
log = logging.getLogger("app")
auth_app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().version
)


@auth_app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        if get_settings().drop_tables:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    log.info("Database Initialized...")


@auth_app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


@auth_app.post("/login")
async def login(
        user: UserLogin,
        session: AsyncSession = Depends(get_session),
        settings: Settings = Depends(get_settings)) -> UserAuthed:
    try:
        result = await UserAccount.login_user(session, settings, user)
    except:
        raise

    return result


@auth_app.post("/user", status_code=201)
async def user_create(
        user: UserCreate,
        session: AsyncSession = Depends(get_session),
        settings: Settings = Depends(get_settings)) -> UserAuthed:
    result = await UserAccount.create_user(session, settings, user)

    if isinstance(result, str):
        raise HTTPException(status_code=404, detail=result)

    return result


@auth_app.get("/user2")
async def user_jwt_get(token: str = Depends(oauth2_scheme)):
    # token = request.headers.get("Authorization")
    # if token is None:
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     raise credentials_exception
    #
    # current_user = await jwt.get_user_from_jwt(settings, token)
    import ipdb;
    ipdb.set_trace()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app", host="0.0.0.0", port=8888,
                log_level="debug", reload=True)
