from fastapi import APIRouter

from backend.posts.routes import router as post_router

routers = APIRouter()
routers.include_router(post_router)
