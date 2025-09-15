from flask import Blueprint, jsonify

from ..models import GPXTrack

bp = Blueprint('gpx', __name__, url_prefix='/api/gpx')


@bp.get('/tracks')
def list_tracks():
    tracks = GPXTrack.query.filter_by(is_public=True).all()
    return jsonify([{'id': t.id, 'name': t.name} for t in tracks])
