from fastapi import APIRouter

from .auth.routes import auth_route
from .post.routes import post_routes
from .users.routes import user_routes
from .connection.routes import conn_routes

routers = APIRouter()
routers.include_router(auth_route)
routers.include_router(post_routes)
routers.include_router(user_routes)
routers.include_router(conn_routes)
routers.include_router(post_routes)
