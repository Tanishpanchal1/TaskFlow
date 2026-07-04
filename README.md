# TaskFlow

Production-ready Task Management Backend built with FastAPI.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Docker
- Redis
- JWT Authentication
- Async Programming

---

## Project Structure

## Setup

### Local

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Copy `.env.example` to `.env` and adjust `DATABASE_URL` if needed.
3. Run the app with `uvicorn app.main:app --reload`.

### Docker

1. Build and start services with `docker compose up --build`.
2. Open the API docs at `/docs`.

## Migrations

Run Alembic with `alembic upgrade head`.

## Tests

Run `pytest` from the repository root.

## Architecture

Request flow: route -> dependency -> CRUD -> ORM model -> response schema -> exception handlers.
