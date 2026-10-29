# TaskFlow

TaskFlow is an asynchronous task-management backend built with FastAPI. It
provides a structured API for organizing work across teams and projects,
assigning tasks, tracking status and priority, and collaborating through task
comments.

The project is designed as a backend/API engineering project rather than a
frontend application. It demonstrates layered service design, async database
access, token-based authentication, schema validation, migrations, and
containerized local development.

## What it supports

- User registration, login, and refresh-token authentication
- Password hashing and JWT access/refresh tokens
- Admin and member roles
- Team creation, membership, and role-aware visibility
- Projects grouped under teams
- Task creation, updates, deletion, assignment, and status changes
- Task priorities, due dates, status filtering, assignee filtering, pagination,
  and project scoping
- Comments attached to tasks
- Pydantic request/response schemas and centralized validation
- Health checks and OpenAPI documentation through FastAPI

## Architecture

TaskFlow follows a layered request flow:

```text
HTTP route
  -> authentication/dependency checks
  -> CRUD service
  -> SQLAlchemy ORM model
  -> Pydantic response schema
  -> database transaction
```

The main application areas are:

```text
app/
├── api/                 # API dependencies and versioned route handlers
│   └── v1/              # auth, users, teams, projects, tasks, comments
├── core/                # settings, constants, security, logging
├── crud/                # reusable async database operations
├── db/                  # async engine, sessions, metadata, initialization
├── models/              # SQLAlchemy entities and relationships
├── schemas/             # Pydantic request and response models
├── middleware/          # application middleware extensions
└── utils/               # permissions and exception helpers
```

The data model is centered on:

```text
User <-> Team -> Project -> Task -> Comment
                         |
                         -> User (assignee)
```

Task and project access is checked against team membership, while admin-only
operations are enforced through role dependencies.

## API areas

The versioned API is mounted at `/api/v1`:

| Area | Examples |
| --- | --- |
| Authentication | Register, login, refresh tokens |
| Users | User lookup and account operations |
| Teams | Admin team management and member visibility |
| Projects | Team-scoped project CRUD |
| Tasks | CRUD, assignment, status changes, filtering |
| Comments | Task collaboration and comment management |

The application also exposes `GET /health` for service checks. When the server
is running, FastAPI publishes interactive API documentation at `/docs` and
`/redoc`.

## Technology

- Python 3.12+
- FastAPI and Uvicorn
- Pydantic v2 and `pydantic-settings`
- SQLAlchemy 2.0 async ORM
- PostgreSQL for containerized development
- SQLite with `aiosqlite` for lightweight local/test configurations
- Alembic database migrations
- Redis configuration for future caching/background work
- JWT authentication with password hashing
- Pytest and `pytest-asyncio`
- Docker Compose

## Running locally

### Prerequisites

- Python 3.12 or newer
- PostgreSQL for the production-like Docker setup, or SQLite for a lightweight
  local setup
- Docker and Docker Compose (optional)

### Local Python setup

```bash
git clone https://github.com/Tanishpanchal1/TaskFlow.git
cd TaskFlow

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

The default settings use a local SQLite database. Set `DATABASE_URL` in `.env`
to use PostgreSQL.

### Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

The Compose configuration starts the API with PostgreSQL and includes a
pgAdmin service for database inspection. The API is available at
`http://localhost:8000`.

### Database migrations

```bash
alembic upgrade head
alembic downgrade -1
```

Migrations currently cover the initial schema, task comments, and task
priority/filter indexes.

## Testing and quality checks

Run the test suite with:

```bash
pytest
```

The repository also includes configuration for Ruff, Black, isort, and mypy.
The Makefile contains the project shortcuts for local development and checks.

## Configuration

Important environment variables include:

```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite+aiosqlite:///./taskflow.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=replace-this-value
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Use a strong secret key and non-default credentials outside local development.
Do not commit `.env` files or production secrets.

## Project status

TaskFlow is an API-focused project with the core authentication, team,
project, task, comment, migration, and test foundations in place. Redis is
configured in the deployment environment, but it is not required for the
basic CRUD and authentication flows.

## License

No license has currently been declared for this repository.
