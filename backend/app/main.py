from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.router import api_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

origins = [
    "http://localhost",
    # Frontend React (por si acaso)
    "http://localhost:3000",
    # Vite (En mi caso utilice este "Vite")
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

# Defini esta ruta de prueba para validar cuando funcione el API, para asi no pasar a trabajar el frontend, ademas lo probe con
# Postman y Curl
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Wikipedia Analyzer",
        "docs": f"{settings.API_PREFIX}/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)