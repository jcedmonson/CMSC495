import logging
from typing import Annotated

from fastapi import APIRouter, Header, status, HTTPException

from data_service.data_app.models import user_account as user_model
from data_service.data_app import dependency_injection as inj
from data_service.data_app.endpoints import crud

log = logging.getLogger("auth_routes_users")
router = APIRouter(prefix="/users")

@router.get("")
async def fetch_all_users(_: inj.CurrentUser_t,
                          session: inj.Session_t) -> list[user_model.User]:
    return await crud.get_all_users(session)


@router.get("/{user_name}")
async def get_user(user_name: str,
                   _: inj.CurrentUser_t,
                   session: inj.Session_t
                   ) -> user_model.User | None:

    return await crud.get_user(session, user_name)

