"""Embeddings Service Module."""

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.services.utilities.logs import get_logger

settings = get_settings()
logger = get_logger(__name__)


class EmbeddingsService:
    """Service for generating text embeddings."""

    def __init__(self):
        """Initialize the embeddings model."""
        logger.info(f"Loading embeddings model: {settings.QDRANT_EMBEDDINGS_MODEL}")
        self.model = SentenceTransformer(settings.QDRANT_EMBEDDINGS_MODEL)
        logger.info("Embeddings model loaded successfully")

    def encode(self, texts: str | list[str]) -> list[list[float]]:
        """Generate embeddings for text(s).

        Args:
            texts: Single text string or list of text strings.

        Returns:
            list[list[float]]: List of embedding vectors.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


# Singleton instance
_embeddings_service = None


def get_embeddings_service() -> EmbeddingsService:
    """Get or create singleton embeddings service instance.

    Returns:
        EmbeddingsService: Singleton embeddings service.
    """
    global _embeddings_service
    if _embeddings_service is None:
        _embeddings_service = EmbeddingsService()
    return _embeddings_service
