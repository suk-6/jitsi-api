from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    # HOST
    host: str = "localhost"
    port: int = 8443

    # Frontend URL
    front_url: str = "http://localhost:5173"

    # JWT
    jwt_app_id: str = "jitsi"
    jwt_app_secret: str = "jitsi"

    # Postgres
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_db: str = "db"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Environment File
    model_config = SettingsConfigDict(env_file=".env")
