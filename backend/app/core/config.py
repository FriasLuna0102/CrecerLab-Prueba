import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Configuraciones de la aplicación cargadas desde variables de entorno o .env"""

    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = os.getenv("DEBUG", False)
    PROJECT_NAME: str = "Wikipedia Analyzer API"
    VERSION: str = "0.1.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    WIKIPEDIA_API_URL: str = os.getenv("WIKIPEDIA_API_URL", "https://en.wikipedia.org/w/api.php")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()