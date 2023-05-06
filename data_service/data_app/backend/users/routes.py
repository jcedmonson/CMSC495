import logging
from typing import Annotated

from fastapi import APIRouter, Header, status, HTTPException
from backend.jwt_validation import jwt_check
from models.user_profile import User
import dependency_injection as inj

log = logging.getLogger("auth_routes_users")
router = APIRouter(prefix="/users")

@router.get("")
async def fetch_all_users(authorization: Annotated[str | None, Header()],
                          oauth2: inj.Token_t,
                          ) -> list[User]:
    try:
        jwt_header = await jwt_check(authorization, oauth2)
    except:
        raise

    result = await oauth2.get("/get_users", headers=jwt_header)
    return result.json()


@router.get("/{user_name}")
async def get_user(user_name: str,
                   authorization: Annotated[str | None, Header()],
                   oauth2: inj.Token_t
                   ) -> User | None:
    try:
        jwt_header = await jwt_check(authorization, oauth2)
    except:
        raise

    result = await oauth2.get(f"/get_user/{user_name}", headers=jwt_header)

    if result.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Query did not produce any results",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result.json()
