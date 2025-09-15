from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from ..extensions import db
from ..models import ChatRoom, ChatMessage

bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@bp.get('/rooms')
@login_required
def list_rooms():
    rooms = ChatRoom.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in rooms])


@bp.get('/rooms/<int:room_id>/messages')
@login_required
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
@login_required
def post_message(room_id: int):
    data = request.get_json() or {}
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Invalid payload'}), 400

    chat_message = ChatMessage(room_id=room_id, user_id=current_user.id, message=message)
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
