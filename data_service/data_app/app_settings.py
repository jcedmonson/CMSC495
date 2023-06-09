import logging
from functools import lru_cache

from pydantic import BaseSettings

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

log = logging.getLogger("app.jwt")

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

@lru_cache()
def get_settings():
    """Settings cache"""
    return Settings()

class Settings(BaseSettings):
    app_name: str = "Data Service -- City Park"
    version: str = "0.0.1"
    postgres_db: str
    postgres_user: str
    postgres_password: str
    pgdata: str
    pgport: int = 5432
    host: str

    drop_tables: bool = False
    log_mode: str = "DEBUG"

    # JWT section
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"],
                                             deprecated=["auto"])

    @property
    def post_limit_size(self) -> int:
        return 2048

    @property
    def comment_limit_size(self) -> int:
        return 1024

    @property
    def post_min_size(self) -> int:
        return 1

    @property
    def comment_min_size(self) -> int:
        return 1

    @property
    def dns(self) -> str:
        return (f"postgresql+asyncpg://"
                f"{self.postgres_user}:{self.postgres_password}"
                f"@{self.host}:{self.pgport}/{self.postgres_db}")

    @property
    def log_settings(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s [%(asctime)s] [Line:%(lineno)d][Func:%(funcName)s] [%(name)s] - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": True
                },

                "app": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True
                },

                "app.jwt": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True
                },

                "endpoint.auth": {
                    "handlers": ["default"],
                    "level": "DEBUG",
                    "propagate": True
                },

                "endpoint.connection": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True
                },

                "endpoint.posts": {
                    "handlers": ["default"],
                    "level": "DEBUG",
                    "propagate": True
                },

                "crud": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True
                },

                "app.db": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True
                },
            }
        }

