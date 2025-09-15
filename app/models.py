"""Application data models.

This module only provides lightweight placeholders for the real models.
The test-suite can monkeypatch the ``query`` attribute of these classes to
simulate database behaviour without requiring a full database setup.
"""


class BaseModel:
    """Simple base class providing a placeholder ``query`` attribute."""

    # The attribute will be replaced by the test-suite or application with an
    # object implementing common query methods (``count``, ``all`` etc.).
    query = None


class User(BaseModel):
    pass


class News(BaseModel):
    pass


class Event(BaseModel):
    pass


class GPXTrack(BaseModel):
    pass
