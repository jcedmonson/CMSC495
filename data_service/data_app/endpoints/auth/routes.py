import logging
from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from endpoints import crud
import dependency_injection as inj
from models import padentic_models as p_models
from . import jwt_token_handler as jwt

log = logging.getLogger("endpoint.auth")
auth_route = APIRouter(prefix="/auth")


@auth_route.post("/login", summary="Authenticate user")
async def login(
        user: p_models.UserLogin,
        session: inj.Session_t,
        settings: inj.Settings_t) -> p_models.UserAuthed:
    """Authenticate a user by providing a username and password"""

    try:
        result = await crud.login_user(session, settings, user)
    except:
        raise

    return result

@auth_route.post("/user", status_code=201, summary="Create a new user")
async def user_create(
        user: p_models.UserCreate,
        session: inj.Session_t,
        settings: inj.Settings_t) -> None:
    result = await crud.create_user(session, settings, user)
    if isinstance(result, str):
        raise HTTPException(status_code=404, detail=result)

    log.debug(f"User {result.user_name} has been created")


@auth_route.get("/user", summary="Validate users JWT token")
async def user_jwt_get(
        current_user: jwt.CurrentUser_t) -> p_models.UserAuthed:
    log.debug(f"User {current_user.user_name} authorized")
    return current_user

@auth_route.post("/token", response_model=p_models.Token,
                 summary="OAuth2 Endpoint")
async def jwt_login(
        form_data: inj.OAuthForm_t,
        session: inj.Session_t,
        settings: inj.Settings_t
):
    """Endpoint is used internally. There is no uppercase where a user would
    need to hit this endpoint at this time"""
    log.debug(f"Authenticating user [{form_data.username}]")

    user = await crud.authenticate_user(session,
                                        settings,
                                        form_data.username,
                                        form_data.password)
    if not user:
        log.debug(f"User {form_data.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    log.debug(f"Successfully authenticated user, [{form_data.username}]")

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)

    access_token = jwt.create_access_token(
        data={"sub": user.user_name},
        settings=settings,
        expires_delta=access_token_expires
    )

    log.debug(f"Created token {access_token}")

    return {"access_token": access_token, "token_type": "bearer"}
