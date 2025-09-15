from datetime import datetime

from geoalchemy2 import Geometry

from ..extensions import db


class GPXTrack(db.Model):
    __tablename__ = 'gpx_tracks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    track_data = db.Column(Geometry('LINESTRING', srid=4326))
    distance_km = db.Column(db.Numeric(8, 3))
    elevation_gain_m = db.Column(db.Integer)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # pragma: no cover
        return f'<GPXTrack {self.name}>'
