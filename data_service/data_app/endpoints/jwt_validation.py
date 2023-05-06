import logging

from fastapi import HTTPException, status
from httpx import AsyncClient

log = logging.getLogger("jwt_validation")


async def jwt_check(authorization: str, oauth2: AsyncClient) -> dict:
    header = {"Authorization": authorization}
    try:
        await validate_jwt(header, oauth2)
    except:
        raise
    return header


async def validate_jwt(jwt_header: dict, oauth2: AsyncClient) -> bool:
    response = await oauth2.get("/user", headers=jwt_header)
    if response.status_code != 200:
        log.debug(f"Invalid token processed: {dict}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
