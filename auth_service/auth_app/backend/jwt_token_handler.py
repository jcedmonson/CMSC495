import json
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from app_settings import Settings, oauth2_scheme, get_settings
from backend import crud
from models.user_account import UserAuthed
from models.jwt_model import TokenData, JWTDBUser
import dependency_injection as inj


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
    encoded_jwt = jwt.encode(to_encode, settings.access_token_expire_minutes,
                             algorithm=settings.algorithm)
    return encoded_jwt


async def get_user_from_jwt(
        token: Annotated[str, Depends(oauth2_scheme)],
        settings: inj.Settings_t,
        session: inj.Session_t
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await crud.get_user(username, session)
    if user is None:
        raise credentials_exception

    return JWTDBUser(username=user.user_name,
                     hashed_password=user.password_hash)


async def get_current_user(
        current_user: Annotated[str, Depends(oauth2_scheme)]) -> UserAuthed:
    pass

    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    # return current_user

# @app.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     return current_user
#
#
# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
