"""REST API routes for schlauDorf."""

from functools import wraps
from typing import Any, Dict, List, Tuple

from flask import Blueprint, abort, jsonify, request
from flask_login import current_user, login_required

from ..models import Event, News, Role, User

bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def admin_required(view):
    """Ensure the current user has administrator privileges."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != Role.ADMIN:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


def paginate_query(query) -> Tuple[List[Any], Dict[str, Any]]:
    """Paginate a SQLAlchemy query using request arguments."""

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    meta = {
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
    }
    return pagination.items, meta


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@bp.errorhandler(403)
def handle_forbidden(_: Exception):
    return jsonify({"error": "forbidden"}), 403


@bp.errorhandler(404)
def handle_not_found(_: Exception):
    return jsonify({"error": "not found"}), 404


# ---------------------------------------------------------------------------
# News routes
# ---------------------------------------------------------------------------

@bp.get("/news")
@login_required
def list_news():
    """Return published news items."""

    query = News.query.filter_by(is_published=True).order_by(News.created_at.desc())
    items, meta = paginate_query(query)
    return jsonify(
        {
            "items": [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "created_at": item.created_at.isoformat(),
                }
                for item in items
            ],
            **meta,
        }
    )


# ---------------------------------------------------------------------------
# Event routes
# ---------------------------------------------------------------------------

@bp.get("/events")
@login_required
def list_events():
    """Return public events."""

    query = Event.query.filter_by(is_public=True).order_by(Event.start_date.desc())
    items, meta = paginate_query(query)
    return jsonify(
        {
            "items": [
                {
                    "id": event.id,
                    "title": event.title,
                    "start_date": event.start_date.isoformat(),
                    "end_date": event.end_date.isoformat() if event.end_date else None,
                    "location": event.location,
                }
                for event in items
            ],
            **meta,
        }
    )


# ---------------------------------------------------------------------------
# User routes
# ---------------------------------------------------------------------------

@bp.get("/users")
@login_required
@admin_required
def list_users():
    """Return a list of all users (admin only)."""

    query = User.query.order_by(User.created_at.desc())
    items, meta = paginate_query(query)
    return jsonify(
        {
            "items": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role.value,
                    "is_verified": user.is_verified,
                }
                for user in items
            ],
            **meta,
        }
    )
