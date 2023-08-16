from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    message_broker_url: str
    default_exchange: str
    default_queue: str
    default_routing_key: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    print("Get settings")
    return AppSettings()


