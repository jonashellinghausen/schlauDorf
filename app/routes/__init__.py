"""Common route utilities and in-memory user storage."""

from typing import Dict

from ..models.user import User

# Very small in-memory storage used for demonstration and testing
# purposes. A real application would employ a persistent database
# instead.
users_db: Dict[int, User] = {}
