from functools import lru_cache

from pydantic import BaseSettings

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache()
def get_settings():
    """Settings cache"""
    return Settings()

class Settings(BaseSettings):
    app_name: str = "Auth Service -- City Park"
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
                    "fmt": "%(levelprefix)s [%(asctime)s] [%(name)s] - %(message)s",
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
                    "level": "DEBUG",
                    "propagate": True
                },

                "app.auth_routes": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": True
                },

                "app.db": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": True
                },
            }
        }

