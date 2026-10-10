# Contributing to Kaléidogram

Thanks for your interest in contributing. This document describes how to set up the project locally and the conventions used in this repository.

## Prerequisites

- **Python**: 3.14 (used in the project's local dev virtual environment). Version 3.14 is pinned via `pyproject.toml` 
- **PostgreSQL**: no specific version is pinned in the repo. Any recent PostgreSQL version (14+) should work.
- **Node.js**: 24 (LTS), the version used by `frontend/Dockerfile`. Vite 8 requires `^20.19.0` or `>=22.12.0`, ESLint 10 requires `^20.19.0`, `^22.13.0` or `>=24`. Only needed for a local setup without Docker.

The project has a `docker-compose.yaml` at the repo root (backend + frontend + PostgreSQL). This is the recommended way to run the project locally — see [Docker setup](#docker-setup) below. A direct/local setup without containers is also documented further down for reference.

## Docker setup

Prerequisites: Docker and Docker Compose (Docker Desktop on macOS/Windows).

1. Clone the repository:

   ```bash
   git clone git@github.com:theKaido/kaleidogram.git
   cd kaleidogram
   ```

2. Create a `.env` file at the repo root (next to `docker-compose.yaml`) with the following variables:

   ```bash
   POSTGRES_USER=<user>
   POSTGRES_PASSWORD=<password>
   POSTGRES_DB=<db-name>
   JWT_SECRET_KEY=<your-secret-key>
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   Then create `frontend/.env` from its template. It holds `VITE_API_URL`, the backend URL the browser calls:

   ```bash
   cp frontend/.env.example frontend/.env
   ```

3. Start the stack:

   ```bash
   docker compose up
   ```

   This builds the backend and frontend images, starts PostgreSQL (with a healthcheck gating backend startup), runs Alembic migrations, then starts the backend dev server with `--reload` and the Vite dev server. The `backend/` and `frontend/` folders are bind-mounted into their containers, so code changes on the host are picked up live.

The API is then available at `http://localhost:8000` (`/docs` for the interactive Swagger UI) and the frontend at `http://localhost:5173`.

To rebuild the backend image after changing `pyproject.toml`/`poetry.lock` or its `Dockerfile`:

```bash
docker compose build backend
docker compose up
```

To rebuild the frontend image after changing `package.json`/`package-lock.json` or its `Dockerfile`, also renew the anonymous `node_modules` volume (otherwise the container keeps the old dependencies):

```bash
docker compose up --build -V frontend
```

To reset the database (wipes all data):

```bash
docker compose down -v
```

## Local setup (without Docker)

Prerequisites: Poetry

1. Clone the repository:

   ```bash
   git clone git@github.com:theKaido/kaleidogram.git
   cd kaleidogram/backend
   ```

2. Install dependencies with poetry (poetry creates a virtual env so you don't need to create one)

   ```bash
   poetry install
   ```

3. Make sure PostgreSQL is running locally. If you don't have a running instance, start one, for example:

   ```bash
   pg_ctl -D /usr/local/var/postgres start
   createdb kaleidogram
   ```

4. Create your local environment file. There is no `.env.example` committed yet — create `backend/.env` manually with the following variables (all read via `os.getenv` in the codebase):

   ```bash
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/kaleidogram
   JWT_SECRET_KEY=<your-secret-key>
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Apply database migrations:

   ```bash
   poetry run alembic upgrade head
   ```

6. Run the dev server:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

The API is then available at `http://127.0.0.1:8000`.

### Frontend

Prerequisites: Node.js 24 (see [Prerequisites](#prerequisites)).

```bash
cd frontend
cp .env.example .env
npm ci
npm run dev
```

`.env` sets `VITE_API_URL`, the backend URL called by the browser (`http://localhost:8000` by default). Restart `npm run dev` after changing it.

The frontend is then available at `http://localhost:5173`. Other scripts: `npm run lint` (ESLint) and `npm run build` (type check with `tsc`, then production build).

## Project structure

```
kaleidogram/
├── CLAUDE.md              # Shared project context
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── docker-compose.yaml
├── .github/
│   └── workflows/         # CI: lint, tests, develop-branch checks
│       ├── develop.yml
│       ├── lint.yml
│       └── tests.yml
├── backend/
│   ├── CLAUDE.md          # Backend-specific conventions
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── poetry.lock
│   ├── alembic.ini
│   ├── alembic/           # Database migrations
│   │   └── versions/
│   ├── tests/             # Pytest suite
│   │   ├── conftest.py
│   │   └── test_*.py
│   └── app/
│       ├── main.py        # FastAPI entry point
│       ├── database.py    # SQLAlchemy setup
│       ├── dependencies/  # FastAPI dependencies (auth, DB session)
│       ├── models/        # SQLAlchemy models
│       ├── routers/       # API endpoints, one module per resource
│       ├── schemas/       # Pydantic schemas (validation/serialization)
│       └── utils/         # Security helpers (password hashing, JWT)
└── frontend/               # React + Vite + TypeScript
    ├── CLAUDE.md          # Frontend-specific conventions
    ├── Dockerfile
    ├── .dockerignore
    ├── package.json
    ├── package-lock.json
    ├── vite.config.ts
    ├── eslint.config.js
    ├── tsconfig*.json
    ├── index.html
    ├── public/
    └── src/
        ├── main.tsx       # React entry point
        ├── App.tsx        # Root component
        └── index.css
```

## Git workflow

This project follows Gitflow:

- `main`: production-ready code only, protected.
- `develop`: default integration branch. Feature/fix branches target this branch.
- Branch naming: `feat/xxx`, `fix/xxx`, `docs/xxx`, `chore/xxx`, branched off `develop`.

Every change goes through a Pull Request, even for solo work on this repo.

## Commit convention

Commits follow [Conventional Commits](https://www.conventionalcommits.org/).

Examples:

```
feat: add JWT authentication on password update endpoint
fix: correct type of sub claim from int to str
docs: add project structure to CLAUDE.md
chore: add python-dotenv dependency
refactor: extract CurrentUser dependency from auth router
```

## Pull request process

1. Open the PR against `develop`, not `main`.
2. Write a clear description: what changed and why, not just what.
3. Make sure the CI is green before requesting review.
4. As the project gains contributors, at least one review will be required before merge. Until then, a self-review of the diff is expected before merging.

## Code style

- **SQLAlchemy**: sync mode with the classic `Session` pattern, no async DB access.
- **Pydantic**: v2 syntax (`model_config = ConfigDict(...)`, `field_validator`).
- **Type hints**: required on all function signatures.
- **Python naming**: snake_case for variables, functions, files, and modules (PEP 8).
- **URL naming**: kebab-case in API paths (e.g. `/plat-ingredient`).
- **Imports**: absolute imports from `app.` (e.g. `from app.models.plat import Plat`).
- **Docstrings**: actually use Google docstring format.

Formatter and linter (Ruff) are configured in this repo. Run these to check linting or formatting code with those commands  
   ```bash
   poetry run ruff check .
   poetry run ruff format --check .
   ```

See [`backend/CLAUDE.md`](backend/CLAUDE.md) for the source of truth on these conventions.

## Running tests

Tests have been added and configured via a `conftest.py` file. To run them, use this command:
   ```bash
   poetry run pytest
   ```


## Reporting issues

Use [GitHub Issues](https://github.com/theKaido/kaleidogram/issues).

When filing a bug report, include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, PostgreSQL version)

When filing a feature request, include:

- The problem you're trying to solve
- The proposed solution, if you have one
- Any alternatives you considered