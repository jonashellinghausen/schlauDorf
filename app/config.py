"""Application configuration module for schlauDorf.

This file exposes the :class:`Config` class used by the application factory
and tests. Configuration values are primarily sourced from environment
variables loaded via ``python-dotenv`` to simplify local development.
"""

import os
from dotenv import load_dotenv


def _str_to_bool(value):
    """Return ``True`` when the string represents a truthy value."""

    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "t", "yes", "on"}

load_dotenv()


class Config:
    """Base configuration loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = _str_to_bool(os.environ.get("FLASK_DEBUG") or os.environ.get("DEBUG"))
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "app/static/uploads")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 52428800))

    WMS_BASE_URL = os.environ.get("WMS_BASE_URL")
    WMS_LAYERS = {
        "luftbild": "rlp_luftbild",
        "topographie": "rlp_dtk",
        "liegenschaft": "rlp_alk",
    }

    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    ADMIN_NAME = "Jonas Hellinghausen"

    @classmethod
    def init_app(cls, app):  # pragma: no cover - default hook for subclasses
        """Hook for subclasses to perform additional validation."""


class ProductionConfig(Config):
    """Configuration for production deployments.

    ``SECRET_KEY`` and ``DATABASE_URL`` must be provided via environment
    variables to avoid insecure defaults when running in production.
    """

    SECRET_KEY = None
    SQLALCHEMY_DATABASE_URI = None
    DEBUG = False

    ENV_VAR_MAPPING = {
        "SECRET_KEY": "SECRET_KEY",
        "SQLALCHEMY_DATABASE_URI": "DATABASE_URL",
    }

    @classmethod
    def init_app(cls, app):
        super().init_app(app)

        missing = []
        for config_key, env_var in cls.ENV_VAR_MAPPING.items():
            value = os.environ.get(env_var)
            if value:
                app.config[config_key] = value
            else:
                missing.append(env_var)

        if missing:
            missing_values = ", ".join(missing)
            raise RuntimeError(
                "ProductionConfig requires the following environment variables to be set: "
                f"{missing_values}"
            )


CONFIG_MAPPINGS = {
    "default": Config,
    "production": ProductionConfig,
}
