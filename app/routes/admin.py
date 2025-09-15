"""Admin routes for managing users and roles."""

from functools import wraps

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Role, User

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    """Decorator ensuring the current user has admin privileges."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != Role.ADMIN:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


@bp.route("/")
@login_required
@admin_required
def dashboard():
    """Display a simple dashboard with user management options."""

    users = User.query.all()
    return render_template("admin/dashboard.html", users=users, roles=list(Role))


@bp.route("/users/<int:user_id>/verify")
@login_required
@admin_required
def verify_user(user_id: int):
    """Mark a user account as verified."""

    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    flash("User verified", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/users/<int:user_id>/role/<role>")
@login_required
@admin_required
def set_role(user_id: int, role: str):
    """Change the role for a given user."""

    user = User.query.get_or_404(user_id)
    try:
        user.role = Role(role)
    except ValueError:
        abort(404)
    db.session.commit()
    flash("Role updated", "success")
    return redirect(url_for("admin.dashboard"))

