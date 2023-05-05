import logging
from typing import Annotated

from fastapi import  APIRouter, Header

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import dependency_injection as inj
from backend.jwt_validation import jwt_check

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/posts")


@router.get("")
async def fetch_test(authorization: Annotated[str | None, Header()],
                     oauth2: inj.Token_t,
                     settings: inj.Settings_t
                     ) -> dict:
    try:
        await jwt_check(authorization, oauth2)
    except:
        raise

    return {"request": "valid"}
