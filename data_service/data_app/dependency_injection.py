from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from endpoints.database import get_session
from app_settings import Settings, get_settings

Session_t = Annotated[AsyncSession, Depends(get_session)]
Settings_t = Annotated[Settings, Depends(get_settings)]
OAuthForm_t = Annotated[OAuth2PasswordRequestForm, Depends()]
