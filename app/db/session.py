"""
Gestionnaire de connexions et de sessions de base de données (SQLAlchemy Async).

Ce module initialise le moteur asynchrone SQLAlchemy (`AsyncEngine`), 
définit la classe déclarative de base pour les modèles ORM, et fournit 
les générateurs de sessions asynchrones pour FastAPI (`get_db_session`).
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Création du moteur asynchrone SQLAlchemy pour PostgreSQL
engine = create_async_engine(
    settings.sqlalchemy_database_url,
    echo=False,
    future=True
)

# Fabrique de sessions asynchrones (AsyncSession)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    """
    Classe déclarative racine pour tous les modèles ORM SQLAlchemy de l'application.
    """

    pass


async def init_db() -> None:
    """
    Initialise la base de données en créant toutes les tables définies
    dans les modèles héritant de `Base` si elles n'existent pas encore.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fournisseur de dépendance FastAPI délivrant une session SQLAlchemy asynchrone.

    Yields:
        AsyncSession: Instance de session asynchrone avec fermeture garantie en fin de requête.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
