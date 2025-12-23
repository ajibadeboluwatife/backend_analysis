# Backend professional

High-accuracy Retrieval-Augmented Generation (RAG) coding assistant built exclusively for backend developers working with Python and FastAPI.

## Project Overview

Backend professional a specialized retrieval-augmented generation (RAG) system designed as a coding assistant for backend developers working with Python and FastAPI. It combines a vector database storing official FastAPI documentation with a local language model to provide accurate, context-grounded answers to technical questions. The system ensures privacy by keeping all data local and focuses exclusively on trusted sources to minimize hallucinations.

## Core Objectives

- Deliver fast, accurate answers to questions about FastAPI, Pydantic, SQLModel, Starlette, async Python, and related technologies
- Prioritize official documentation and internal code examples over generic training data
- Eliminate hallucinations on framework-specific behavior through strict source grounding
- Serve as a self-hosted, fully controllable alternative to commercial coding assistants
- Support seamless incremental updates as the team's codebase and knowledge evolve
- Guarantee complete data privacy — no external API calls containing proprietary code or documentation

## Documentation

- **[Backend Documentation](./backend/README.md)** - FastAPI server, Qdrant integration, and RAG pipeline
- **[Frontend Documentation](./frontend/README.md)** - React UI, API client, and Docker setup


## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ajibadeboluwatife/backend_professional.git
   cd backend_professional
   ```

2. **Create environment files:**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Start all services:**
   ```bash
   make build
   # or: docker compose up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Qdrant: http://localhost:6333/dashboard

### Manual Setup

See individual documentation:
- [Backend Setup](./backend/README.md#setup)
- [Frontend Setup](./frontend/README.md#setup)


### Prerequisites

- Python 3.12+
- Node.js 18+
- Docker & Docker Compose

## Architecture

```
┌─────────────────────┐
│   React Frontend    │
│   (Port 3000)       │
└──────────┬──────────┘
           │
           │ HTTP/REST
           │
┌──────────▼──────────┐
│   FastAPI Backend   │
│   (Port 8000)       │
│  - Health check     │
│  - Chat endpoint    │
│  - Ingestion API    │
└──────────┬──────────┘
           │
           │ gRPC
           │
┌──────────▼──────────┐
│ Qdrant Vector DB    │
│ (Port 6333)         │
│ - Document storage  │
│ - Semantic search   │
└─────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: FastAPI + Uvicorn
- **Vector Database**: Qdrant
- **Embeddings**: Sentence Transformers

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: CSS3
- **Server**: Nginx

## Key Features

- Full-stack RAG system with semantic search
- Modern React UI with real-time chat
- Self-hosted and fully private
- Automatic documentation ingestion
- Docker-ready deployment
- Fast vector search with Qdrant
- Local language model integration
