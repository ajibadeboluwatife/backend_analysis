# Backend Professional

A full-stack example project combining a Python backend (Backend Professional) and a Vite-powered frontend.  
This README focuses on quick onboarding, consistent local development, and reproducible builds.

> Quick summary
- Backend: Python (FastAPI-style layout), uses pydantic-based settings and environment variables.
- Frontend: Vite + TypeScript (served with nginx in production).
- Dev convenience: Docker & docker-compose included for easy local runs.

Table of contents
- Prerequisites
- Quick start (local)
- Quick start (Docker)
- Configuration (.env)
- Development tasks (lint, test, build)
- CI / GitHub Actions
- Contributing & style
- License & contact

Prerequisites
- Python 3.11+ (recommended)
- Node.js 18+ and npm (for frontend)
- Docker & Docker Compose (for containerized dev and production)
- git

Quick start — run locally (recommended for development)
1. Clone
   git clone https://github.com/ajibadeboluwatife/backend_professional.git
   cd backend_professional

2. Backend (example)
   - Create and activate a virtual environment:
     python -m venv .venv
     source .venv/bin/activate   # macOS/Linux
     .venv\Scripts\activate      # Windows (PowerShell)
   - Install dependencies
     - If Backend/requirements.txt exists:
       pip install -r Backend/requirements.txt
     - Otherwise install your project's dependencies as appropriate.
   - Provide a .env file (see Configuration below).
   - Start (example using uvicorn; adjust import path if different):
     uvicorn Backend.App.main:app --reload --port 8000
   - Tests (if present):
     pytest -q Backend

3. Frontend
   cd Frontend
   # use lockfile if present for reproducible installs
   if [ -f package-lock.json ]; then npm ci; else npm install; fi
   # development server
   npm run dev
   # build for production
   npm run build
   # preview production build (if configured)
   npm run preview --if-present

Quick start — Docker / docker-compose
- Build and run everything with Docker Compose:
  docker-compose up --build
- Or build and run frontend and backend containers separately:
  docker build -t backend -f Backend/Dockerfile Backend
  docker build -t frontend -f Frontend/Dockerfile Frontend

Configuration (.env)
This project uses environment variables. Create a `.env` at the repository root (or in `Backend/`) with the following recommended entries (values shown are defaults found in code — override as needed):

```
# Backend settings
APP_API_PREFIX=/api/v1
APP_NAME=Backend Professional
APP_VERSION=1.0.0
DEBUG=false

# Qdrant (vector DB) settings
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=backend-Professional
QDRANT_BATCH_SIZE=64
QDRANT_DIM=384
EMBEDDINGS_BACKEND=local
EMBEDDINGS_MODEL=all-MiniLM-L6-v2

# Ollama (llm host) settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b
```

Note: The exact names and defaults are defined in `Backend/App/Core/config.py`. If `config.py` still contains APP_NAME="Backend Oracle" and you want consistency, I can prepare a patch to update that default as well — tell me if you'd like me to change code defaults too.

Development tasks and recommended tooling
- Linting & formatting:
  - Python: black, isort, ruff/flake8
  - JS/TS: eslint, prettier
  Add a `.pre-commit-config.yaml` to run these automatically on commits.
- Tests:
  - Keep tests in `Backend/tests` and run via `pytest`.
  - Use `pytest -q Backend` (this is used in CI).
- Docker image best practices (applies to Frontend Dockerfile):
  - Copy `package-lock.json` before `npm ci` to leverage Docker caching.
  - Use multi-stage builds and serve the built site from nginx's standard webroot.
- Dependency pinning:
  - Commit lockfiles: `package-lock.json` for frontend, and `requirements.txt` or `poetry.lock` for backend for reproducible builds.

CI / GitHub Actions
A simple starter workflow is in `.github/workflows/ci.yml` (example provided below). It runs backend tests and builds frontend with caching to reduce run time.

Contributing
- Fork the repo, create a feature branch, run tests & linters locally, and open a PR with a clear description.
- Use small, focused PRs. Add tests for bug fixes or new functionality.

Notes / Known issues & quick wins
- Fix package initializer typo:
  - Ensure `Backend/App/Core/__init__.py` exists (there is currently `__innit__.py` which should be renamed). This will avoid import problems.
- Frontend Dockerfile improvements:
  - Use `npm ci` when lockfile exists, copy manifest before install to leverage caching, and serve from `/usr/share/nginx/html`.
- Add GitHub Actions caching for pip and npm to speed up CI runs.

License
This repository includes a LICENSE file. Please see `LICENSE` for details.

Contact
If you want me to prepare PRs for:
- renaming `__innit__.py` -> `__init__.py`
- optimized `Frontend/Dockerfile`
- adding `.github/workflows/ci.yml` starter
tell me and I’ll prepare the patches/PRs.
