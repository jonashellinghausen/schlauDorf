import pytest

from app import create_app
from app.config import Config, ProductionConfig


class CustomConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def test_production_config_requires_env(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError):
        create_app(ProductionConfig)


def test_production_config_loads_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "super-secret")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    app = create_app(ProductionConfig)

    assert app.config["SECRET_KEY"] == "super-secret"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_flask_config_env_missing_variables(monkeypatch):
    monkeypatch.setenv("FLASK_CONFIG", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError):
        create_app()


def test_create_app_uses_flask_config(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "prod-secret")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("FLASK_CONFIG", "production")

    app = create_app()

    assert app.config["SECRET_KEY"] == "prod-secret"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"

    monkeypatch.setenv("FLASK_CONFIG", "tests.test_config.CustomConfig")

    app = create_app()

    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
