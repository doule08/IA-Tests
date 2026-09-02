from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and configuration."""

    api_title: str = "ToDo List API"
    api_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    
    # Path to storing data
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = base_dir / "data"
    todos_file_path: Path = data_dir / "todos.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
