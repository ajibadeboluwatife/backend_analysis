"""RAG Chain Module for Context Retrieval."""

from app.services.embeddings import get_embeddings_service
from app.services.qdrant_service import get_qdrant_service
from app.services.utilities.logs import get_logger

logger = get_logger(__name__)


async def retrieve_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant context from the vector database.

    Args:
        query: User's question or query.
        top_k: Number of top results to retrieve.

    Returns:
        str: Concatenated context from retrieved documents.
    """
    try:
        # Get services
        embeddings_service = get_embeddings_service()
        qdrant_service = get_qdrant_service()
        
        # Generate query embedding
        logger.info(f"Generating embedding for query: {query[:50]}...")
        query_embedding = embeddings_service.encode(query)[0]
        
        # Search for similar documents
        logger.info(f"Searching for top {top_k} similar documents")
        results = qdrant_service.search(query_embedding, limit=top_k)
        
        if not results:
            logger.warning("No results found in vector database")
            return "No relevant documentation found. Please ensure the knowledge base has been populated."
        
        # Extract and concatenate context
        context_parts = []
        for idx, result in enumerate(results, 1):
            score = result.get("score", 0)
            payload = result.get("payload", {})
            text = payload.get("text", payload.get("content", ""))
            source = payload.get("source", "Unknown")
            
            if text:
                context_parts.append(
                    f"[Source {idx} - Score: {score:.3f} - {source}]\n{text}\n"
                )
        
        context = "\n---\n".join(context_parts)
        logger.info(f"Retrieved {len(results)} documents, total context length: {len(context)}")
        
        return context
        
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return f"Error retrieving context: {str(e)}"
