from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Global SQLAlchemy instance
db = SQLAlchemy()


def create_app():
    """Factory to create and configure the Flask application."""
    app = Flask(__name__)
    db.init_app(app)

    # Import and register blueprints lazily to avoid circular imports
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
