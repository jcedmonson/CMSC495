from fastapi import APIRouter

from data_app.backend.authentication.views import router as auth_router

routers = APIRouter()
routers.include_router(auth_router)
