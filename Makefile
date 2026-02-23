.PHONY: setup dev dev-backend dev-frontend test test-backend test-frontend lint migrate migration seed clean

setup:
	docker compose up -d
	cd backend && uv sync --all-extras
	cd frontend && npm install
	@echo "\n✓ Setup complete. Copy .env.example files and edit as needed."

dev:
	$(MAKE) -j2 dev-backend dev-frontend

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	$(MAKE) test-backend
	$(MAKE) test-frontend

test-backend:
	cd backend && uv run pytest -v

test-frontend:
	cd frontend && npm run test:run

lint:
	cd backend && uv run ruff check .
	cd backend && uv run mypy app/
	cd frontend && npm run lint

migrate:
	cd backend && uv run alembic upgrade head

migration:
	cd backend && uv run alembic revision --autogenerate -m "$(m)"

seed:
	cd backend && uv run python scripts/seed.py

clean:
	docker compose down -v
	rm -rf backend/.venv backend/__pycache__
	rm -rf frontend/node_modules frontend/.next
