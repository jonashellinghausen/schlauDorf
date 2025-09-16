from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sys

try:  # pragma: no cover - prefer stdlib sqlite
    import sqlite3 as _sqlite3
except Exception:  # pragma: no cover - stdlib sqlite missing
    _sqlite3 = None

sqlite3 = _sqlite3
if sqlite3 is None or not hasattr(sqlite3.Connection, "enable_load_extension"):
    try:  # pragma: no cover - optional pysqlite fallback
        import pysqlite3 as sqlite3  # type: ignore
    except ImportError:  # pragma: no cover - fall back to stdlib even without extensions
        if _sqlite3 is None:  # pragma: no cover - both modules missing
            raise
        sqlite3 = _sqlite3
    else:
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
            try:
                dbapi_conn.enable_load_extension(True)
                dbapi_conn.load_extension("mod_spatialite")
            except Exception:  # pragma: no cover - extension unavailable
                pass
