from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from endpoints.database import get_session
from app_settings import Settings, get_settings
from models import user_account
from endpoints.auth import jwt_token_handler as jwt

Session_t = Annotated[AsyncSession, Depends(get_session)]
Settings_t = Annotated[Settings, Depends(get_settings)]
CurrentUser_t = Annotated[user_account.UserAuthed, Depends(jwt.get_current_user)]
OAuthForm_t = Annotated[OAuth2PasswordRequestForm, Depends()]
