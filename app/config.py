from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8443
    jwt_app_id: str = "jitsi"
    jwt_app_secret: str = "jitsi"
    model_config = SettingsConfigDict(env_file=".env")
