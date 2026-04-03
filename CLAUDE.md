# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jira Clone Backend API built with FastAPI, PostgreSQL, SQLAlchemy ORM, Alembic migrations, and JWT authentication. Package management uses **uv**.

## Common Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Database migrations
alembic upgrade head          # Apply all pending migrations
alembic downgrade -1          # Rollback one migration
alembic revision --autogenerate -m "description"  # Generate new migration

# Seed default admin user (otsiadmin@otsi.co.in / Admin@123)
python app/scripts/seed_admin.py

# Install dependencies
uv sync
```

## Architecture

### Request Flow
```
HTTP Request → app/main.py → app/api/v1/api.py (router) → endpoints/ → services/ → db/
```

### Layer Responsibilities

- **`app/api/v1/endpoints/`** — Route handlers; delegate business logic to services, use deps for auth
- **`app/services/`** — Business logic (currently `auth_service.py`); no direct HTTP concerns
- **`app/models/`** — SQLAlchemy ORM models (User, Project, ProjectMember)
- **`app/schemas/`** — Pydantic request/response models (validation and serialization)
- **`app/api/deps.py`** — FastAPI dependencies: `get_db()` (DB session), `get_current_user()` (JWT auth)
- **`app/core/config.py`** — Pydantic `BaseSettings` loaded from `.env`
- **`app/db/base.py`** — Imports all models so Alembic autogenerate detects them

### Authentication & Authorization
- JWT tokens (HS256) via `python-jose`; tokens expire in 30 min (configurable)
- `get_current_user` dependency extracts user from Bearer token — inject it to protect any route
- Admin-only routes check `current_user.is_admin`
- Project-level access checks if the user has a `ProjectMember` record; PM role required for member management

### Database Models & Relationships
```
User ──< ProjectMember >── Project
          role: PM | DESIGNER | FE | BE | DEVOPS | QA
          unique(user_id, project_id)
```

When creating a project, the creator is automatically added as a `PM` in `ProjectMember`.

### Adding a New Feature (typical pattern)
1. Add/update model in `app/models/` and import it in `app/db/base.py`
2. Run `alembic revision --autogenerate -m "..."` and `alembic upgrade head`
3. Add Pydantic schemas in `app/schemas/`
4. Add service functions in `app/services/` (or create a new service file)
5. Add endpoint file in `app/api/v1/endpoints/` and register router in `app/api/v1/api.py`

## Environment Configuration

Copy `.env` and adjust for your environment. Required variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=<random secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Structure

All routes are prefixed with `/api/v1`.

| Prefix | File | Access |
|--------|------|--------|
| `/auth` | `endpoints/auth.py` | Public |
| `/users` | `endpoints/users.py` | Admin or authenticated |
| `/projects` | `endpoints/projects.py` | Authenticated |
