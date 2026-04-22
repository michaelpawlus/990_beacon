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

## `beacon` CLI

An agent-facing wrapper over the FastAPI backend. Installed as a console script
from `backend/` (`pipx install -e backend` or `uv pip install -e backend`).

**Environment:**

- `BEACON_API_URL` — backend base URL (default `http://localhost:8000`)
- `BEACON_API_TOKEN` — Clerk JWT, copied from the signed-in web app (devtools
  → Network → any authed request → `Authorization: Bearer ...`)

Global flags: `--base-url`, `--token`, `--timeout`. Every read command accepts
`--json` (JSON to stdout; human text to stderr otherwise). Exit codes: `0`
success, `1` error (auth / network / server), `2` not found.

| Command | Example |
|---|---|
| `beacon health` | `beacon health --json` |
| `beacon whoami` | `beacon whoami --json` (auth smoke test) |
| `beacon search QUERY` | `beacon search "food bank" --state OH --json \| jq '.total'` |
| `beacon typeahead QUERY` | `beacon typeahead "typ" --json` (min length 2) |
| `beacon org ein EIN` | `beacon org ein 310123456 --json` |
| `beacon org show ORG_ID` | `beacon org show <uuid> --json` |
| `beacon usage` | `beacon usage --json` |
