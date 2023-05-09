import logging

from fastapi import APIRouter, Header, status, HTTPException

from models import padentic_models as p_model
import dependency_injection as inj
from endpoints.auth.jwt_token_handler import CurrentUser_t
from endpoints import crud

log = logging.getLogger("endpoint.connection")
conn_routes = APIRouter(prefix="/connections")


@conn_routes.get("/user/{user_id}")
async def get_users_connections(
        user_id: int,
        _: CurrentUser_t,
        session: inj.Session_t) -> list[p_model.User] | None:

    try:
        results = await crud.get_connections(session, user_id)
        log.info(f"User ID {user_id} has {len(results)}")
        return results
    except:

        log.error(f"User {user_id} was not found")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username not found",
            headers={"WWW-Authenticate": "Bearer"},
        )


@conn_routes.post("/user", status_code=201)
async def create_connection(
        user_to_add: p_model.User,
        current_user: CurrentUser_t,
        session: inj.Session_t) -> None:

    log.debug(f"Creating connection for {current_user.user_id} to {user_to_add.user_id}")
    try:
        await crud.set_connection(session, current_user, user_to_add)
    except:
        raise
