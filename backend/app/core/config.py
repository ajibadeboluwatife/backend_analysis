"""Backend Oracle Application Configurations."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    APP_API_PREFIX: str = "/api/v1"
    APP_DESCRIPTION: str = "Coding Assistant for Backend Developers"
    APP_NAME: str = "Backend Oracle"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    QDRANT_BATCH_SIZE: int = 64
    QDRANT_COLLECTION: str = "backend-Professional"
    QDRANT_DIM: int = 384
    QDRANT_EMBEDDINGS_BACKEND: str = os.getenv("EMBEDDINGS_BACKEND", "local").lower()
    QDRANT_EMBEDDINGS_MODEL: str = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "gemma:2b")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get or create a cached Settings instance.

    Returns:
        Settings: Cached application settings instance.
    """
    return Settings()
