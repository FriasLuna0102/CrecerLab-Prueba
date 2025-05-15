from fastapi import FastAPI
from app.api import articles_router, search_router
from app.core.config import settings

def include_routers(app: FastAPI):
    """
    Incluye todos los routers en la aplicación FastAPI
    """
    app.include_router(articles_router, prefix=settings.API_PREFIX)
    app.include_router(search_router, prefix=settings.API_PREFIX)