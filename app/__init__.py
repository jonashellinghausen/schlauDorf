from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'

    from .routes.event import event_bp
    app.register_blueprint(event_bp)

    return app
