from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # DeepSeek
    deepseek_api_key: str
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # PostgreSQL
    database_url: str

    # Chroma
    chroma_persist_dir: str = ".chroma"

    # App
    app_name: str = "墨境 Storycraft"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()