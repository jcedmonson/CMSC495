import logging
from typing import Annotated

from fastapi import  APIRouter, Header
from backend.jwt_validation import jwt_check
import dependency_injection as inj

log = logging.getLogger("auth_routes_users")
router = APIRouter(prefix="/users")

@router.get("")
async def fetch_all_users(authorization: Annotated[str | None, Header()],
                     oauth2: inj.Token_t,
                     settings: inj.Settings_t
                     ) -> dict:
    try:
        await jwt_check(authorization, oauth2)
    except:
        raise

    return {"request": "valid"}
