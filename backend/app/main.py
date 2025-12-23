"""Backend Oracle FastAPI Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routes import api_router
from app.services.utilities.logs import get_logger

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Args:
        app: FastAPI application instance.
    """
    logger.info("Starting Backend Oracle API")
    
    # Initialize services on startup
    try:
        from app.services.embeddings import get_embeddings_service
        from app.services.qdrant_service import get_qdrant_service
        
        # Initialize services
        get_embeddings_service()
        get_qdrant_service()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
    
    yield
    
    logger.info("Shutting down Backend Oracle API")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.APP_API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint.

    Returns:
        dict: Welcome message and API information.
    """
    return {
        "message": "Welcome to Backend Oracle API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.APP_API_PREFIX}/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
