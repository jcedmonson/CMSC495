from datetime import datetime, timedelta
from typing import Annotated
import logging

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app_settings import Settings, oauth2_scheme, get_settings
from endpoints import crud
from models import user_account as user_model
from models.jwt_model import TokenData, JWTDBUser, JWTUser
import dependency_injection as inj

log = logging.getLogger("app.jwt")


def verify_password(settings: Settings, plain_password: str,
                    hashed_password: bytes) -> bool:
    return settings.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(settings: Settings, password: str) -> bytes:
    return settings.pwd_context.hash(password).encode("UTF-8")


def create_access_token(data: dict,
                        settings: Settings,
                        expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             settings.secret_key,
                             algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: inj.Session_t,
        settings: inj.Settings_t
) -> user_model.UserAuthed:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception


    user = await crud.get_user(session, token_data.username)
    if user is None:
        raise credentials_exception

    # Set the token for the user
    user.token = token
    await session.commit()
    await session.refresh(user)

    log.debug(f"Authenticated user {user_model.UserAuthed(**user.__dict__)}")

    return user_model.UserAuthed(**user.__dict__)

async def get_current_active_user(
        current_user: Annotated[user_model.UserAuthed, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

CurrentUser_t = Annotated[user_model.UserAuthed, Depends(get_current_user)]
