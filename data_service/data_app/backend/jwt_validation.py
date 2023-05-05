import logging

from fastapi import HTTPException, status
from httpx import AsyncClient

log = logging.getLogger("jwt_validation")


async def jwt_check(authorization: )
async def validate_jwt(jwt_header: str, oauth2: AsyncClient) -> bool:
    response = await oauth2.get("/user", headers=jwt)
    if response.status_code != 200:
        log.debug(f"Invalid token processed: {dict}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
