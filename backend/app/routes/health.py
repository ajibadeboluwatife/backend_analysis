"""Health Check Route Module."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        dict: Health status.
    """
    return {"status": "healthy", "service": "Backend Oracle API"}
