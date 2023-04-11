import logging

from fastapi import Depends, HTTPException, APIRouter

from data_app.models.user_profile import UserLogin, UserProfile
from data_app.backend.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/login")


# @router.post("")
# async def login(data: UserLogin,
#                 session: AsyncSession = Depends(get_session),
#                 use_case: CreateUser = Depends(CreateUser)) -> str:
#     print(data)
#     return "Hi"

@router.post("")
async def login(data: UserLogin,
                session: AsyncSession = Depends(get_session)) -> str:
    result = await UserProfile.login_user(session,
                                          data.user_name,
                                          data.password)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    return "Working"
