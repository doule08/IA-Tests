"""
Modèles ORM SQLAlchemy pour l'entité Todo.

Ce module définit la structure des tables en base de données PostgreSQL 
représentant les tâches ToDo.
"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TodoModel(Base):
    """
    Modèle ORM représentant la table `todos` en base de données PostgreSQL.

    Attributes:
        id (str): Identifiant unique UUIDv4 de la tâche (clé primaire).
        title (str): Titre / Intitulé de la tâche (max 200 caractères).
        description (Optional[str]): Description détaillée optionnelle.
        is_completed (bool): Statut de réalisation (par défaut False).
        created_at (datetime): Horodatage avec fuseau horaire de la création.
        updated_at (datetime): Horodatage avec fuseau horaire de la dernière mise à jour.
    """

    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
