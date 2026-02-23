# CLAUDE.md — 990 Beacon

## Project Overview

990 Beacon is a subscription intelligence platform that transforms IRS 990 nonprofit filing data into actionable insights for fundraisers, prospect researchers, grant writers, and nonprofit consultants.

## Tech Stack

- **Frontend:** Next.js 15 (App Router), TypeScript, Tailwind CSS v4, shadcn/ui
- **Auth:** Clerk
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic
- **Database:** PostgreSQL 16
- **Cache:** Redis 7
- **Testing:** Vitest + Testing Library (frontend), pytest + pytest-asyncio (backend)
- **Package management:** uv (backend), npm (frontend)
- **CI:** GitHub Actions

## Project Structure

```
990_beacon/
├── frontend/          # Next.js 15 app
├── backend/           # FastAPI app
├── docs/              # Documentation (PRD, etc.)
├── docker-compose.yml # Local dev services (Postgres, Redis)
├── Makefile           # Dev commands
└── CLAUDE.md          # This file
```

## Architecture Decisions

- Monorepo with separate frontend/ and backend/ directories
- Clerk for auth (handles sign-up/in, JWTs, webhooks for user sync)
- PostgreSQL with pg_trgm for fuzzy name search
- Async SQLAlchemy for all DB operations; sync psycopg for Alembic migrations
- Separate test Postgres container on port 5433

## Patterns & Conventions

- Backend uses FastAPI dependency injection for DB sessions and auth
- All API routes versioned under `/api/v1/`
- Clerk webhooks verified with svix
- Frontend components in `src/components/`, pages in `src/app/`
- shadcn/ui for component primitives

## Commands

```bash
make setup        # Install all dependencies
make dev          # Start frontend + backend
make test         # Run all tests
make lint         # Lint frontend + backend
make migrate      # Run Alembic migrations
```
