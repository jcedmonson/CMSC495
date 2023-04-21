import logging
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, Header, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app_settings_data import get_settings, get_oauth2_session
import dependency_injection as inj

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/posts")


async def validate_jwt(jwt: dict, oauth2: AsyncClient) -> bool:
    response = await oauth2.get("/user", headers=jwt)
    if response.status_code != 200:
        log.debug(f"Invalid token processed: {dict}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


@router.get("")
async def fetch_test(authorization: Annotated[str | None, Header()],
                     oauth2: inj.Token_t,
                     settings: inj.Settings_t
                     ) -> dict:
    header = {"Authorization": authorization}
    try:
        await validate_jwt(header, oauth2)
    except:
        raise

    return {"request": "valid"}
