"""Qdrant Vector Database Service Module."""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import get_settings
from app.services.utilities.logs import get_logger

settings = get_settings()
logger = get_logger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        """Initialize Qdrant client and ensure collection exists."""
        logger.info(f"Connecting to Qdrant at {settings.QDRANT_URL}")
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the collection exists, create if it doesn't."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.QDRANT_DIM,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection {self.collection_name} created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise

    def search(self, query_vector: list[float], limit: int = 5) -> list[dict]:
        """Search for similar vectors in the collection.

        Args:
            query_vector: Query embedding vector.
            limit: Maximum number of results to return.

        Returns:
            list[dict]: List of search results with scores and payloads.
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            return [
                {
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in results
            ]
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {e}")
            return []

    def add_documents(self, documents: list[dict], embeddings: list[list[float]]):
        """Add documents with embeddings to the collection.

        Args:
            documents: List of document dictionaries with text and metadata.
            embeddings: List of embedding vectors corresponding to documents.
        """
        try:
            points = [
                PointStruct(
                    id=idx,
                    vector=embedding,
                    payload=doc
                )
                for idx, (doc, embedding) in enumerate(zip(documents, embeddings))
            ]
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Added {len(points)} documents to collection")
        except Exception as e:
            logger.error(f"Error adding documents to Qdrant: {e}")
            raise


# Singleton instance
_qdrant_service = None


def get_qdrant_service() -> QdrantService:
    """Get or create singleton Qdrant service instance.

    Returns:
        QdrantService: Singleton Qdrant service.
    """
    global _qdrant_service
    if _qdrant_service is None:
        _qdrant_service = QdrantService()
    return _qdrant_service
