from fastapi import APIRouter

from auth_app.backend.views import router as auth_router

routers = APIRouter()
routers.include_router(auth_router)
