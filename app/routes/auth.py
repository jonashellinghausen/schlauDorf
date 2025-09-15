"""Authentication routes including email verification."""
from flask import Blueprint, jsonify, request

from ..models.user import User
from . import users_db


auth_bp = Blueprint("auth", __name__)


def send_verification_email(user: User) -> None:
    """Placeholder for sending verification emails.

    In a real application this would send an actual email. For development
    and testing purposes we simply print the token so that it can be used
    by the client to confirm the account.
    """
    print(f"Verification token for {user.email}: {user.verification_token}")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a user and issue a verification token."""
    data = request.get_json(force=True)
    user = User(id=len(users_db) + 1, email=data["email"], password=data["password"])
    users_db[user.id] = user
    send_verification_email(user)
    return jsonify({"message": "User created. Verification email sent."}), 201


@auth_bp.route("/verify/<token>")
def verify(token: str):
    """Verify a user's email address using a token."""
    for user in users_db.values():
        if user.verify(token):
            return jsonify({"message": "Account verified."})
    return jsonify({"error": "Invalid or expired token."}), 400
