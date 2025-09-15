from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models import ChatRoom, ChatMessage

bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@bp.get('/rooms')
def list_rooms():
    rooms = ChatRoom.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in rooms])


@bp.get('/rooms/<int:room_id>/messages')
def get_messages(room_id: int):
    messages = (
        ChatMessage.query.filter_by(room_id=room_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return jsonify([
        {
            'id': m.id,
            'user_id': m.user_id,
            'message': m.message,
            'created_at': m.created_at.isoformat(),
        }
        for m in messages
    ])


@bp.post('/rooms/<int:room_id>/messages')
def post_message(room_id: int):
    data = request.get_json() or {}
    message = data.get('message')
    user_id = data.get('user_id')
    if not message or not user_id:
        return jsonify({'error': 'Invalid payload'}), 400

    chat_message = ChatMessage(room_id=room_id, user_id=user_id, message=message)
    db.session.add(chat_message)
    db.session.commit()

    return (
        jsonify(
            {
                'id': chat_message.id,
                'user_id': chat_message.user_id,
                'message': chat_message.message,
                'created_at': chat_message.created_at.isoformat(),
            }
        ),
        201,
    )
