from flask import Flask
from flask_socketio import SocketIO

from .socket_events import init_socketio
from .routes.chat import chat_bp

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'  # In production use environment variable

    app.register_blueprint(chat_bp)

    socketio.init_app(app)
    init_socketio(socketio)

    return app
