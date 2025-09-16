import os

from flask import Flask
from werkzeug.utils import import_string

from .config import CONFIG_MAPPINGS, Config
from .extensions import db, migrate, login_manager, socketio, csrf


def _load_config_from_string(config_name: str):
    config_class = CONFIG_MAPPINGS.get(config_name)
    if config_class is not None:
        return config_class
    return import_string(config_name)


def _resolve_config_class(config_class):
    if config_class is None:
        config_name = os.environ.get("FLASK_CONFIG")
        if not config_name:
            return Config
        return _load_config_from_string(config_name)
    if isinstance(config_class, str):
        return _load_config_from_string(config_class)
    return config_class


def create_app(config_class=None) -> Flask:
    """Application factory for the schlauDorf project."""
    resolved_config = _resolve_config_class(config_class)

    app = Flask(__name__)
    app.config.from_object(resolved_config)
    if hasattr(resolved_config, "init_app"):
        resolved_config.init_app(app)

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)

    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .routes.legal import bp as legal_bp
    app.register_blueprint(legal_bp)

    from .routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .routes.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    from .routes.maps import bp as maps_bp
    app.register_blueprint(maps_bp)

    try:  # GPX routes depend on spatial libraries
        from .routes.gpx import bp as gpx_bp
        app.register_blueprint(gpx_bp)
    except Exception:  # pragma: no cover - optional dependency missing
        pass

    from .routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from .routes.api import bp as api_bp
    app.register_blueprint(api_bp)

    # Import Socket.IO event handlers
    from . import socket_events  # noqa: F401

    return app
