import logging

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger("auth_routes")
router = APIRouter(prefix="/posts")


@router.get("")
async def login() -> str:
    return "Working"
