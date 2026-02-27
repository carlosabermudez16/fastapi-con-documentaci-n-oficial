from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENVIRONMENT: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    SLACK_WEBHOOK_URL: str | None = None
    AUTH0_DOMAIN: str | None = None
    AUTH0_AUDIENCE: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # 👈 permite variables extra
    )


settings = Settings()  # para usar en lógica de negocio y test


# para usar en endpoints
@lru_cache
def get_settings() -> Settings:
    return settings
