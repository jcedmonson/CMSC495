from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from httpx import AsyncClient

from backend.database import get_session
from app_settings_data import Settings, get_settings, get_oauth2_session

Session_t = Annotated[AsyncSession, Depends(get_session)]
Settings_t = Annotated[Settings, Depends(get_settings)]
Token_t = Annotated[AsyncClient, Depends(get_oauth2_session)]
