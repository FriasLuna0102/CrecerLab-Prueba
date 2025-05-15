from typing import Optional

from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import ConfigDict

class Settings(BaseSettings):
    API_PREFIX: str = "/test_api"
    DEBUG: bool = False
    PROJECT_NAME: str = "Wikipedia Analyzer API"
    VERSION: str = "0.1.0"
    DATABASE_URL: str
    WIKIPEDIA_API_URL: str = "https://en.wikipedia.org/w/api.php"
    SECRET_KEY: Optional[str] = None


    model_config = ConfigDict(env_file=".env", case_sensitive=True)

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()