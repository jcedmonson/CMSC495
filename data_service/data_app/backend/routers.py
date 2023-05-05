from fastapi import APIRouter

from backend.posts.routes import router as post_router
from backend.users.routes import router as users_router

routers = APIRouter()
routers.include_router(post_router)
routers.include_router(users_router)
