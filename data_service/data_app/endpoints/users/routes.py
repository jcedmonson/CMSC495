import logging
from typing import Annotated

from fastapi import APIRouter, Header, status, HTTPException

from models import padentic_models as p_model
import dependency_injection as inj
from endpoints.auth.jwt_token_handler import CurrentUser_t
from endpoints import crud

log = logging.getLogger("auth_routes_users")
user_routes = APIRouter(prefix="/users")


@user_routes.get("/{user_name}")
async def get_user(user_name: str,
                   _: CurrentUser_t,
                   session: inj.Session_t
                   ) -> list[p_model.User] | None:
    try:
        return await crud.get_user(session, user_name, exact_match=False)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


@user_routes.get("")
async def fetch_all_users(_: CurrentUser_t,
                          session: inj.Session_t) -> list[p_model.User]:

    return await crud.get_all_users(session)
