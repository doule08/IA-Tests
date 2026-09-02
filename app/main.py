from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API RESTful ToDo List développée avec FastAPI et une architecture propre (Controller -> Service -> Repository).",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour autoriser l'accès ultérieur par des frontends / backends consommateurs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement du routeur v1
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["healthcheck"])
async def root():
    """Endpoint racine pour vérifier la santé de l'API."""
    return {
        "message": "Bienvenue sur l'API ToDo List!",
        "docs": "/docs",
        "version": settings.api_version
    }
