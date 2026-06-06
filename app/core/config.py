from pathlib import Path

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_HOST: str
    DATABASE_PORT: int = 5432

    UV_NO_DEV: int = 0

    @property
    @computed_field
    def DATABASE_URL(self) -> str:
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.POSTGRES_DB,
        )
        return str(dsn)


settings = Settings()  # type: ignore
