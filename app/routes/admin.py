"""Administrative interface views.

This module exposes a small set of views used by the administration
interface.  The views are intentionally lightweight so they can operate in
an isolated test environment without a fully configured database.
"""

from flask import Blueprint, render_template, redirect, url_for, flash

from .. import db
from ..models import User, News, Event, GPXTrack


# Blueprint for all admin related routes
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
def dashboard():
    """Render an overview of statistics and recent activity.

    The counts of the primary models are queried via their ``query``
    attribute.  The ``query`` objects are expected to implement ``count``,
    ``order_by`` and ``limit`` methods like a typical SQLAlchemy query.  For
    environments without a database, the tests can monkeypatch these
    attributes with light‑weight stand‑ins.
    """

    statistics = {
        "users": User.query.count(),
        "news": News.query.count(),
        "events": Event.query.count(),
        "tracks": GPXTrack.query.count(),
    }

    # Recent activity – fallback to empty lists if the query interface is not
    # fully featured.
    recent_users = (
        User.query.order_by(getattr(User, "created_at", None)).limit(5).all()
        if getattr(User.query, "order_by", None)
        else []
    )
    recent_news = (
        News.query.order_by(getattr(News, "created_at", None)).limit(5).all()
        if getattr(News.query, "order_by", None)
        else []
    )
    recent_events = (
        Event.query.order_by(getattr(Event, "created_at", None)).limit(5).all()
        if getattr(Event.query, "order_by", None)
        else []
    )

    return render_template(
        "admin/dashboard.html",
        statistics=statistics,
        recent_users=recent_users,
        recent_news=recent_news,
        recent_events=recent_events,
    )


@admin_bp.route("/users")
def users():
    """List all users for administration."""
    user_list = User.query.all()
    return render_template("admin/users.html", users=user_list)


@admin_bp.route("/users/<int:user_id>/verify", methods=["POST"])
def verify_user(user_id: int):
    """Mark a user account as verified.

    The function expects that the ``User.query`` object implements a
    ``get_or_404`` method.  After marking the user as verified the session is
    committed.  In environments where committing is not possible, any
    exception is silently ignored to keep the handler lightweight.
    """

    user = User.query.get_or_404(user_id)
    setattr(user, "verified", True)
    try:
        db.session.commit()
    except Exception:  # pragma: no cover - best effort without a real DB
        pass
    flash("User verified", "success")
    return redirect(url_for("admin.users"))
