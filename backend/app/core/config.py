from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://beacon:beacon@localhost:5432/beacon_dev"
    DATABASE_URL_SYNC: str = "postgresql+psycopg://beacon:beacon@localhost:5432/beacon_dev"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://beacon:beacon@localhost:5433/beacon_test"
    REDIS_URL: str = "redis://localhost:6379/0"
    CLERK_SECRET_KEY: str = ""
    CLERK_WEBHOOK_SECRET: str = ""
    FRONTEND_URL: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"


settings = Settings()
