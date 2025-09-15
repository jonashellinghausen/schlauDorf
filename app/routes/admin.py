"""Administrative routes for managing user accounts."""
from flask import Blueprint, abort, jsonify, request

from ..models.user import Role
from . import users_db

admin_bp = Blueprint("admin", __name__)


def _require_admin():
    """Ensure that the requester is an administrator.

    The admin's user id can be provided via the `X-Admin-Id` header or an
    `admin_id` query parameter. In a real application, authentication
    would be handled through sessions or tokens.
    """
    admin_id = request.headers.get("X-Admin-Id") or request.args.get("admin_id")
    if not admin_id:
        abort(403)
    admin = users_db.get(int(admin_id))
    if not admin or admin.role is not Role.ADMIN:
        abort(403)
    return admin


@admin_bp.route("/approve/<int:user_id>", methods=["POST"])
def approve_user(user_id: int):
    """Approve a user by marking them as verified."""
    _require_admin()
    user = users_db.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.is_verified = True
    return jsonify({"message": "User approved."})


@admin_bp.route("/revoke/<int:user_id>", methods=["POST"])
def revoke_user(user_id: int):
    """Revoke a user's verification status."""
    _require_admin()
    user = users_db.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.is_verified = False
    return jsonify({"message": "User revoked."})
