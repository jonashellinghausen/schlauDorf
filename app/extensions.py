from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sys

try:  # pragma: no cover - pysqlite fallback
    import sqlite3
    if not hasattr(sqlite3.Connection, "enable_load_extension"):
        raise ImportError
except Exception:  # pragma: no cover - default to pysqlite3
    import pysqlite3 as sqlite3  # type: ignore
    sys.modules["sqlite3"] = sqlite3

# Initialize extensions without app for factory pattern

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*")
csrf = CSRFProtect()


# SpatiaLite support for SQLite databases
if hasattr(sqlite3.Connection, "enable_load_extension"):
    @event.listens_for(Engine, "connect")
    def load_spatialite(dbapi_conn, connection_record):  # pragma: no cover - optional dependency
        if isinstance(dbapi_conn, sqlite3.Connection):
            dbapi_conn.enable_load_extension(True)
            dbapi_conn.load_extension("mod_spatialite")
