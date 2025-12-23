# Backend Oracle - Backend Documentation

High-accuracy Retrieval-Augmented Generation (RAG) coding assistant backend built for developers working with Python and FastAPI.

## Overview

The backend service provides a FastAPI-based REST API that combines:
- Vector database (Qdrant) for semantic search
- Local embeddings generation using Sentence Transformers
- LLM integration via Ollama for natural language responses
- RAG pipeline for context-aware answers

## Architecture

```
FastAPI Backend (Port 8000)
├── /api/v1/health       - Health check endpoint
├── /api/v1/chat         - Chat with RAG context
└── Services
    ├── Embeddings       - Generate text embeddings
    ├── Qdrant           - Vector database operations
    └── Chain            - RAG context retrieval
```

## Project Structure

```
backend/
├── app/
│   ├── core/            # Configuration and settings
│   ├── models/          # Pydantic models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   │   ├── embeddings.py       # Sentence Transformers
│   │   ├── qdrant_service.py   # Vector DB operations
│   │   └── utilities/
│   │       ├── chain.py        # RAG retrieval
│   │       ├── logs.py         # Logging utilities
│   │       └── prompts.py      # System prompts
│   └── main.py          # Application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── .env.example        # Environment variables template
```

## Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (for containerized setup)

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application Settings
APP_NAME=Backend Oracle
DEBUG=False

# Qdrant Settings
QDRANT_URL=http://qdrant:6333
QDRANT_COLLECTION=backend-Professional
QDRANT_DIM=384

# Embeddings Settings
EMBEDDINGS_MODEL=all-MiniLM-L6-v2

# Ollama Settings
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=gemma:2b
```

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start required services:**
   ```bash
   # Start Qdrant
   docker run -p 6333:6333 qdrant/qdrant:latest
   
   # Start Ollama
   docker run -p 11434:11434 ollama/ollama
   ollama pull gemma:2b
   ```

3. **Run the application:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/v1/health

### Docker Deployment

Use the provided Docker Compose setup from the root directory:

```bash
# From repository root
docker compose up --build
```

## API Endpoints

### Health Check
```http
GET /api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Backend Oracle API"
}
```

### Chat
```http
POST /api/v1/chat
```

Request:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I create a FastAPI endpoint?"
    }
  ]
}
```

Response:
```json
{
  "message": {
    "role": "assistant",
    "content": "To create a FastAPI endpoint..."
  },
  "model": "gemma:2b",
  "done": true
}
```

## Key Features

### RAG Pipeline
1. **Query Processing**: User question is converted to embeddings
2. **Context Retrieval**: Semantic search in Qdrant for relevant docs
3. **Response Generation**: LLM generates answer using retrieved context
4. **Greeting Detection**: Bypasses RAG for casual greetings

### Embeddings
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Fast local inference using Sentence Transformers
- Optimized for semantic similarity

### Vector Database
- Qdrant for efficient semantic search
- COSINE distance metric
- Automatic collection management

## Development

### Adding New Routes

Create a new route file in `app/routes/`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
async def example():
    return {"message": "Example endpoint"}
```

Register it in `app/routes/__init__.py`:
```python
from app.routes.example import router as example_router
api_router.include_router(example_router, tags=["example"])
```

### Adding New Services

Create service files in `app/services/` following the singleton pattern used in `embeddings.py` and `qdrant_service.py`.

## Testing

### Manual Testing

Use the interactive API docs at `/docs` or use curl:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

## Troubleshooting

### Common Issues

1. **Connection to Qdrant fails**
   - Ensure Qdrant is running on port 6333
   - Check `QDRANT_URL` in `.env`

2. **Ollama timeout**
   - Increase timeout in chat.py
   - Ensure Ollama has the model pulled: `ollama pull gemma:2b`

3. **Embeddings model download**
   - First run downloads the model (~90MB)
   - Check internet connection

4. **Port already in use**
   - Change port in docker-compose.yaml or stop conflicting service

## Performance

- Average response time: 2-5 seconds (depends on context size and model)
- Concurrent requests: Limited by Uvicorn workers
- Memory usage: ~2GB (model + embeddings + app)

## Security

- CORS enabled for development (restrict in production)
- No authentication (add JWT/OAuth for production)
- Environment variables for sensitive config
- No external API calls (fully self-hosted)

## License

See LICENSE file in repository root.
