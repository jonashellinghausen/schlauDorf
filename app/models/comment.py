from datetime import datetime
from .. import db


class Comment(db.Model):
    """Comment on a news item."""
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    author = db.Column(db.String(80))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Back reference to news item
    news = db.relationship('News', back_populates='comments')
