from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and configuration."""

    api_title: str = "ToDo List API"
    api_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    # PostgreSQL Configuration
    postgres_server: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "todo_db"
    
    # Optional direct Database URL override
    database_url: Optional[str] = None

    # Path for fallback JSON data storage
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = base_dir / "data"
    todos_file_path: Path = data_dir / "todos.json"

    @property
    def sqlalchemy_database_url(self) -> str:
        """Construct SQLAlchemy async PostgreSQL connection URL."""
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


settings = Settings()

