"""
Agrégateur des routes API de la version 1 (v1).

Ce module centralise l'enregistrement de l'ensemble des sous-routeurs 
d'endpoints (ex: todos, users, etc.) sous l'espace de nommage `/api/v1`.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import todos

api_router = APIRouter()
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
