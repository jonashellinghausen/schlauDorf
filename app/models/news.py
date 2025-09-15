from datetime import datetime
from .. import db


class News(db.Model):
    """News item model."""
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    image_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to comments
    comments = db.relationship(
        'Comment', back_populates='news', cascade='all, delete-orphan', lazy=True
    )
