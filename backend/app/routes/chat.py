"""Chat Route Module."""

import httpx
from fastapi import APIRouter, HTTPException, Request

from app.core.config import get_settings
from app.models.chat import ChatRequest
from app.services.utilities.chain import retrieve_context
from app.services.utilities.logs import get_logger
from app.services.utilities.prompts import SYSTEM_PROMPT

settings = get_settings()
logger = get_logger(__name__)
router = APIRouter()


def is_greeting(question: str) -> bool:
    """Check if the question appears to be a greeting."""
    greetings = ["hello", "hi", "hey", "how are you", "good morning", "good afternoon", "good evening", "what's up", "sup"]
    question_lower = question.lower().strip()
    # Check for exact greeting words or very short casual greetings
    return any(greet in question_lower for greet in greetings) or (len(question.split()) <= 3 and question_lower in ["hi", "hello", "hey", "yo"])


@router.post("/chat")
async def chat(request: ChatRequest, raw_request: Request = None):
    """Handle chat requests with RAG context.

    Args:
        request: ChatRequest containing messages.
        raw_request: Raw request for debugging

    Returns:
        dict: Chat completion response from Ollama.

    Raises:
        HTTPException: If no messages are provided.
    """
    if not request.messages:
        logger.error("No messages provided in chat request")
        raise HTTPException(400, "No messages provided")

    user_question = request.messages[-1].content
    logger.info(f"User question: {user_question}")
    
    # Skip context retrieval for greetings to allow natural LLM responses
    if is_greeting(user_question):
        context = "Greeting detected - respond naturally as an AI assistant."
        logger.info("Greeting detected, using natural response mode")
    else:
        context = await retrieve_context(user_question)
        logger.info(f"Retrieved context length: {len(context)}")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": f"Relevant documentation:\n\n{context}"},
        {"role": "user", "content": user_question},
    ]

    payload = {
        "model": settings.OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.1},
    }

    async with httpx.AsyncClient() as client:
        
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
               json=payload,
               timeout=120.0
        )
        logger.info(f"Ollama response status: {response.status_code}")
        if response.status_code != 200:
            logger.error(f"Ollama error response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Ollama API error: {response.text}",
            )
        result = response.json()
        logger.info(f"Ollama response: {result}")
        return result
