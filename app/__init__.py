from flask import Flask

from .extensions import limiter
from .routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config.setdefault('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})

    # Register extensions
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp)

    return app
