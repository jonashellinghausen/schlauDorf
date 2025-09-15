from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Database instance

db = SQLAlchemy()


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'
    app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)

    with app.app_context():
        # Import models to register them with SQLAlchemy
        from .models import News, Comment  # noqa: F401
        db.create_all()

        from .routes.news import news_bp
        app.register_blueprint(news_bp)

    return app
