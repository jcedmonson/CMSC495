import logging.config
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from backend.database import database, get_session
from models.user_account import UserAccount, UserCreate, UserLogin, UserAuthed
from app_settings import Settings, get_settings
import backend.jwt_token_handler as jwt


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


@auth_app.get("/user")
async def user_jwt_get(
        current_user: Annotated[UserAuthed, Depends(jwt.get_user_from_jwt)]
) -> UserAuthed:
    return current_user


@auth_app.post("/token")
async def jwt_login(
        session: AsyncSession = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends()) -> dict | None:
    # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": "LKJALKJ", "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app", host="0.0.0.0", port=8888,
                log_level="debug", reload=True)
