from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from app_settings import Settings, get_settings

Session_t = Annotated[AsyncSession, Depends(get_session)]
Settings_t = Annotated[Settings, Depends(get_settings)]
