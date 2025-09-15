from flask import Flask

from .config import Config
from .extensions import db, migrate, login_manager, socketio, csrf


def create_app(config_class: type = Config) -> Flask:
    """Application factory for the schlauDorf project."""
    app = Flask(__name__)
    app.config.from_object(config_class)

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

    from .routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .routes.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    from .routes.maps import bp as maps_bp
    app.register_blueprint(maps_bp)

    from .routes.gpx import bp as gpx_bp
    app.register_blueprint(gpx_bp)

    from .routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from .routes.api import bp as api_bp
    app.register_blueprint(api_bp)

    # Import Socket.IO event handlers
    from . import socket_events  # noqa: F401

    return app
