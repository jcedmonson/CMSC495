import logging

from fastapi import  APIRouter

from data_service.data_app import dependency_injection as inj

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/posts")


@router.get("")
async def fetch_test(authed_user: inj.CurrentUser_t) -> dict:
    return {"request": "valid"}
