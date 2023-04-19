import logging.config
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import database, get_session
from backend import crud
import backend.jwt_token_handler as jwt
from models.user_account import UserCreate, UserLogin, UserAuthed
from models.jwt_model import JWTDBUser
from models.base import Base
from app_settings import Settings, get_settings
import dependency_injection as inj

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
        result = await crud.login_user(session, settings, user)
    except:
        raise

    return result


@auth_app.post("/user", status_code=201)
async def user_create(
        user: UserCreate,
        session: AsyncSession = Depends(get_session),
        settings: Settings = Depends(get_settings)) -> UserAuthed:
    result = await crud.create_user(session, settings, user)

    if isinstance(result, str):
        raise HTTPException(status_code=404, detail=result)

    return result


@auth_app.get("/user")
async def user_jwt_get(
        current_user: Annotated[JWTDBUser, Depends(jwt.get_user_from_jwt)]
) -> JWTDBUser:
    return current_user


@auth_app.post("/token")
async def jwt_login(
        session: inj.Session_t,
        settings: inj.Settings_t,
        form_data: OAuth2PasswordRequestForm = Depends()
) -> dict | None:
    user = await crud.authenticate_user(session,
                                        form_data.username,
                                        form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)

    access_token = jwt.create_access_token(
        data={"sub": user.username},
        settings=settings,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app", host="0.0.0.0", port=8888,
                log_level="debug", reload=True)
