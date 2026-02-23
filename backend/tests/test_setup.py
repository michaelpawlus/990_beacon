from app.core.config import settings


def test_config_loads():
    assert settings.DATABASE_URL is not None
    assert "beacon" in settings.DATABASE_URL


def test_app_imports():
    from app.main import app

    assert app is not None
    assert app.title == "990 Beacon API"
