"""
Module de configuration globale de l'application ToDo List.

Ce module charge et valide les variables d'environnement (fichiers .env) 
à l'aide de Pydantic Settings (BaseSettings) et fournit l'objet `settings`
utilisé à travers toute l'application.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Gestionnaire centralisé des paramètres et configurations de l'application.

    Attributes:
        api_title (str): Titre de l'API affiché dans la documentation OpenAPI.
        api_version (str): Version de l'application API.
        api_v1_prefix (str): Préfixe d'URL pour les endpoints v1.
        postgres_server (str): Hôte / Serveur PostgreSQL.
        postgres_port (int): Port d'écoute du serveur PostgreSQL.
        postgres_user (str): Nom d'utilisateur PostgreSQL.
        postgres_password (str): Mot de passe PostgreSQL.
        postgres_db (str): Nom de la base de données PostgreSQL.
        database_url (Optional[str]): Surcharge optionnelle de la chaîne de connexion DB.
        base_dir (Path): Chemin racine du projet.
        data_dir (Path): Chemin du dossier de données local.
        todos_file_path (Path): Chemin vers le fichier de secours JSON.
    """

    api_title: str = "ToDo List API"
    api_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    # Configuration du serveur PostgreSQL
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "todo_db"

    # Option de surdéfinition directe de la chaîne de connexion
    database_url: Optional[str] = None

    # Chemins des répertoires du projet
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = base_dir / "data"
    todos_file_path: Path = data_dir / "todos.json"

    @property
    def sqlalchemy_database_url(self) -> str:
        """
        Génère dynamiquement l'URL de connexion asynchrone pour SQLAlchemy (asyncpg).

        Returns:
            str: Chaîne de connexion PostgreSQL au format 'postgresql+asyncpg://...'.
        """
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Singleton de configuration utilisé dans toute l'application
settings = Settings()
