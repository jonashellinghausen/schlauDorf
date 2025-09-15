from datetime import datetime

from ..extensions import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    location_lat = db.Column(db.Numeric(10, 8))
    location_lng = db.Column(db.Numeric(11, 8))
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    max_participants = db.Column(db.Integer)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # pragma: no cover
        return f'<Event {self.title}>'
