import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from data_service.models.user_profile import UserLogin
from data_service.backend.authentication.cruds import CreateUser
from data_service.backend.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/login")


@router.post("")
async def login(data: UserLogin,
                session: AsyncSession = Depends(get_session),
                use_case: CreateUser = Depends(CreateUser)) -> str:
    await use_case.execute(data)
    return "Hi"
