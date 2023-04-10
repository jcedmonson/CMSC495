from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "City Park"
    version: str = "0.0.1"
    postgres_db: str
    postgres_user: str
    postgres_password: str
    pgdata: str
    host: str

    drop_tables: bool = False

    class Config:
        env_file = "../db-service/db_compose.env"
        env_file_encoding = "UTF-8"

    @property
    def dns(self) -> str:
        return (f"postgresql+asyncpg://"
                f"{self.postgres_user}:{self.postgres_password}"
                f"@{self.host}/{self.postgres_db}")
