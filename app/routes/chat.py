from flask import Blueprint, jsonify

from ..models import ChatRoom

bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@bp.get('/rooms')
def list_rooms():
    rooms = ChatRoom.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in rooms])
