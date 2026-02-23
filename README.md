# 990 Beacon

Subscription intelligence platform for IRS 990 nonprofit filing data.

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ with [uv](https://docs.astral.sh/uv/)
- Node.js 22+ with npm

### Setup

```bash
# Clone and enter the repo
git clone <repo-url> && cd 990_beacon

# Start Postgres and Redis
docker compose up -d

# Install dependencies
make setup

# Copy and edit environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
# Edit both files with your Clerk keys

# Run database migrations
make migrate

# (Optional) Seed sample data
make seed

# Start development servers
make dev
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API docs: http://localhost:8000/docs

## Commands

| Command | Description |
|---|---|
| `make setup` | Install all dependencies |
| `make dev` | Start frontend + backend |
| `make test` | Run all tests |
| `make lint` | Lint frontend + backend |
| `make migrate` | Run database migrations |
| `make migration m="desc"` | Create new migration |
| `make seed` | Seed sample data |
| `make clean` | Remove all containers and build artifacts |

## Project Structure

```
990_beacon/
├── frontend/          # Next.js 15 (TypeScript, Tailwind, shadcn/ui)
├── backend/           # FastAPI (Python 3.12, SQLAlchemy, Alembic)
├── docs/              # PRD and documentation
├── docker-compose.yml # Postgres + Redis for local dev
├── Makefile           # Dev commands
├── CLAUDE.md          # AI assistant context
└── CHANGELOG.md       # Phase completion log
```
