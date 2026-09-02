"""
Point d'entrée principal de l'application FastAPI ToDo List.

Ce module instancie l'application FastAPI, configure les middlewares (CORS),
gère les événements de cycle de vie (lifespan DB) et inclut le routeur d'API v1.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Gestionnaire d'événement de cycle de vie (Lifespan) de l'application FastAPI.

    Initialise les tables de la base de données PostgreSQL au démarrage de l'application.

    Args:
        _app (FastAPI): Instance de l'application FastAPI.
    """
    try:
        await init_db()
    except Exception as e:
        print(f"[Warning] Impossible d'initialiser les tables au démarrage : {e}")
    yield


# Instance principale de l'application FastAPI
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API RESTful ToDo List développée avec FastAPI et une architecture propre (Controller -> Service -> Repository).",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuration du middleware CORS pour autoriser les requêtes cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ingestion des routes v1
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["healthcheck"])
async def root():
    """
    Endpoint racine de contrôle de santé (Healthcheck).

    Returns:
        dict: Message de bienvenue, lien vers la doc et version de l'API.
    """
    return {
        "message": "Bienvenue sur l'API ToDo List!",
        "docs": "/docs",
        "version": settings.api_version
    }
