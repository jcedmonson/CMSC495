import logging
from typing import Annotated

from fastapi import  APIRouter, Header
from backend.jwt_validation import jwt_check
from models.user_profile import User
import dependency_injection as inj

log = logging.getLogger("auth_routes_users")
router = APIRouter(prefix="/users")

@router.get("")
async def fetch_all_users(authorization: Annotated[str | None, Header()],
                     oauth2: inj.Token_t,
                     settings: inj.Settings_t
                     ) -> list[User]:
    try:
        jwt_header = await jwt_check(authorization, oauth2)
    except:
        raise

    result =  await oauth2.get("/get_users", headers=jwt_header)
    return result.json()

