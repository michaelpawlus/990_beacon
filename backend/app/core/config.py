from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://beacon:beacon@localhost:5432/beacon_dev"
    DATABASE_URL_SYNC: str = "postgresql+psycopg://beacon:beacon@localhost:5432/beacon_dev"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://beacon:beacon@localhost:5433/beacon_test"
    REDIS_URL: str = "redis://localhost:6379/0"  # Use rediss:// for TLS (Upstash)
    CLERK_SECRET_KEY: str = ""
    CLERK_WEBHOOK_SECRET: str = ""
    CLERK_JWKS_URL: str = ""
    FRONTEND_URL: str = "http://localhost:3000"
    SENTRY_DSN: str = ""
    ENVIRONMENT: str = "development"


settings = Settings()
