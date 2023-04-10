from typing import Annotated, AsyncIterator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker

from data_service.backend.database import get_session
from data_service.models.user_profile import UserAuthed, UserLogin

AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]


class CreateUser:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, post: UserLogin) -> None:
        async with self.async_session.begin() as session:
            print(post.email)

