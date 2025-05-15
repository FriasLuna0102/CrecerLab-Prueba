import logging
from logging.config import dictConfig
import os
from app.core.config import settings


def configure_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    log_dir = "logs"

    # Crear directorio de logs si no existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": f"{log_dir}/app.log",
                "maxBytes": 10485760,  # 10 MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "app": {"handlers": ["console", "file"], "level": log_level},
            "uvicorn": {"handlers": ["console", "file"], "level": log_level},
            "sqlalchemy.engine": {
                "handlers": ["console", "file"],
                "level": logging.WARNING,
            },
        },
    }

    dictConfig(log_config)