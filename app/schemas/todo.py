"""
Schémas de validation Pydantic v2 pour l'entité Todo.

Ce module contient les modèles de données utilisés pour sérialiser, 
désérialiser et valider les requêtes et réponses de l'API REST.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """
    Schéma de base contenant les attributs communs d'une tâche ToDo.

    Attributes:
        title (str): Titre de la tâche (1 à 200 caractères).
        description (Optional[str]): Description détaillée optionnelle (max 1000 caractères).
        is_completed (bool): État d'accomplissement (False par défaut).
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Titre de la tâche ToDo",
        examples=["Acheter du pain"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Description détaillée de la tâche",
        examples=["Passer à la boulangerie du coin avant 19h"]
    )
    is_completed: bool = Field(
        default=False,
        description="Statut d'accomplissement de la tâche"
    )


class TodoCreate(TodoBase):
    """
    Schéma utilisé pour la création d'une nouvelle tâche ToDo (`POST /api/v1/todos/`).
    Hérite directement de `TodoBase`.
    """

    pass


class TodoUpdate(BaseModel):
    """
    Schéma utilisé pour la mise à jour partielle ou totale d'une tâche (`PUT /api/v1/todos/{todo_id}`).
    Tous les champs sont optionnels.

    Attributes:
        title (Optional[str]): Nouveau titre optionnel.
        description (Optional[str]): Nouvelle description optionnelle.
        is_completed (Optional[bool]): Nouveau statut optionnel.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Nouveau titre de la tâche"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Nouvelle description de la tâche"
    )
    is_completed: Optional[bool] = Field(
        default=None,
        description="Nouveau statut d'accomplissement"
    )


class TodoResponse(TodoBase):
    """
    Schéma retourné dans les réponses de l'API REST.

    Attributes:
        id (str): Identifiant unique UUIDv4.
        created_at (datetime): Date et heure UTC de création.
        updated_at (datetime): Date et heure UTC de dernière modification.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Identifiant unique UUID de la tâche"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Horodatage UTC de création de la tâche"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Horodatage UTC de dernière modification"
    )

    model_config = {
        "from_attributes": True
    }
