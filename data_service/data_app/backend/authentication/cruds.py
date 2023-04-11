from fastapi import HTTPException

from data_service.data_app.models.user_profile import UserLogin, UserProfile

# AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]


class CreateUser:
    def __init__(self, session) -> None:
        self.async_session = session

    async def execute(self, post: UserLogin) -> None:
        async with self.async_session.begin() as session:
            result = await UserProfile.login_user(session, post.user_name, post.password)
            if not result:
                raise HTTPException(status_code=404, detail="User not found")



