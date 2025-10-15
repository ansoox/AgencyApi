import os
from functools import lru_cache
from pathlib import Path


class Settings:
    """Simple settings container sourced from environment variables."""

    def __init__(self) -> None:
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:postgres@localhost:5432/agency",
        )
        self.superuser_password: str = os.getenv("SUPERUSER_PASSWORD", "admin")
        self.backup_dir: Path = Path(os.getenv("BACKUP_DIR", "backups"))
        self.csv_dir: Path = Path(os.getenv("CSV_DIR", "exports"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
