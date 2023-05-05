import logging.config
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import database, get_session
from backend import crud
import backend.jwt_token_handler as jwt
from models.user_account import UserCreate, UserLogin, UserAuthed, UserAcc
from models.jwt_model import Token
from models.base import Base
from app_settings import Settings, get_settings
import dependency_injection as inj

logging.config.dictConfig(get_settings().log_settings)
log = logging.getLogger("app")
log.setLevel(get_settings().log_mode)


auth_app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().version,
)

@auth_app.on_event("startup")
async def startup() -> None:
    async with database.engine.begin() as conn:
        if get_settings().drop_tables:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)
    log.info("Database Initialized...")


@auth_app.post("/login", summary="Authenticate user")
async def login(
        user: UserLogin,
        session: inj.Session_t,
        settings: inj.Settings_t) -> UserAuthed:
    """Authenticate a user by providing a username and password"""

    try:
        result = await crud.login_user(session, settings, user)
    except:
        raise

    return result


@auth_app.post("/user", status_code=201, summary="Create a new user")
async def user_create(
        user: UserCreate,
        session: AsyncSession = Depends(get_session),
        settings: Settings = Depends(get_settings)) -> None:

    result = await crud.create_user(session, settings, user)
    if isinstance(result, str):
        raise HTTPException(status_code=404, detail=result)

    log.debug(f"User {result.user_name} has been created")


@auth_app.get("/user", summary="Validate users JWT token")
async def user_jwt_get(
        current_user: Annotated[UserAuthed, Depends(jwt.get_current_user)]
) -> UserAuthed:
    log.debug(f"Processing request from {current_user}")
    return current_user


@auth_app.get("/get_users", summary="Fetch all users")
async def get_all_users(
        current_user: Annotated[UserAuthed, Depends(jwt.get_current_user)],
        session: inj.Session_t,
) -> list[UserAcc]:

    result = await crud.get_all_users(session)
    return result

@auth_app.post("/token", response_model=Token, summary="OAuth2 Endpoint")
async def jwt_login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: inj.Session_t,
        settings: inj.Settings_t
):
    """Endpoint is used internally. There is no uppercase where a user would
    need to hit this endpoint at this time"""
    log.debug(f"Authenticating user [{form_data.username}]")

    user = await crud.authenticate_user(session,
                                        settings,
                                        form_data.username,
                                        form_data.password)
    if not user:
        log.debug(f"User {form_data.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    log.debug(f"Successfully authenticated user, [{form_data.username}]")

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)

    access_token = jwt.create_access_token(
        data={"sub": user.user_name},
        settings=settings,
        expires_delta=access_token_expires
    )

    log.debug(f"Created token {access_token}")

    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:auth_app",
                host="0.0.0.0",
                port=8888,
                reload=True)
