from dataclasses import dataclass, field
from enum import Enum
import secrets


class Role(str, Enum):
    """User roles within the application."""
    USER = "user"
    ADMIN = "admin"


def _generate_token() -> str:
    """Create a cryptographically secure verification token."""
    return secrets.token_urlsafe(32)


@dataclass
class User:
    """Simple user model with verification token and role support."""

    id: int
    email: str
    password: str
    role: Role = Role.USER
    is_verified: bool = False
    verification_token: str = field(default_factory=_generate_token)

    def generate_verification_token(self) -> str:
        """Regenerate a new verification token for the user."""
        self.verification_token = _generate_token()
        self.is_verified = False
        return self.verification_token

    def verify(self, token: str) -> bool:
        """Mark the user as verified if the token matches."""
        if token and secrets.compare_digest(token, self.verification_token):
            self.is_verified = True
            self.verification_token = ""
            return True
        return False
