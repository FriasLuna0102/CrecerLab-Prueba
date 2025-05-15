from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import articles, search
import logging

from app.core.logging import configure_logging


def create_app() -> FastAPI:

    configure_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API para buscar, analizar y guardar artículos de Wikipedia",
        version=settings.VERSION,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_tags=[
            {
                "name": "Articles",
                "description": "Operaciones con artículos guardados",
            },
            {
                "name": "Search",
                "description": "Búsqueda de artículos en Wikipedia",
            },
        ],
    )

    # Configurar CORS
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar routers
    app.include_router(articles.router, prefix=settings.API_PREFIX)
    app.include_router(search.router, prefix=settings.API_PREFIX)

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    @app.get("/")
    async def root():
        return {
            "message": f"Bienvenido a la API de {settings.PROJECT_NAME}",
            "docs": f"{settings.API_PREFIX}/docs"
        }

    return app