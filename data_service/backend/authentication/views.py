import logging

from fastapi import APIRouter, Depends

from data_service.models.user_profile import UserLogin
from data_service.backend.authentication.cruds import CreateUser

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/login")


@router.post("")
async def login(data: UserLogin,
                use_case: CreateUser = Depends(CreateUser)) -> str:

    await use_case.execute(data)

    return "Hi"
