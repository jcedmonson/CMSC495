import logging

from fastapi import  APIRouter

from endpoints.auth.jwt_token_handler import CurrentUser_t

log = logging.getLogger("auth_routes")
post_routes = APIRouter(prefix="/posts")


@post_routes.get("")
async def fetch_test(authed_user: CurrentUser_t) -> dict:
    return {"request": "valid"}
