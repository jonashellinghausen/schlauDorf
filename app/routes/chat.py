from flask import Blueprint, jsonify, request, render_template

from ..storage import messages

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/api/chat/rooms/<room_id>/messages', methods=['GET', 'POST'])
def room_messages(room_id):
    """Retrieve or post messages for a specific room."""
    if request.method == 'POST':
        data = request.get_json() or {}
        username = data.get('username', 'Anonymous')
        text = data.get('message', '')
        record = {'username': username, 'message': text}
        messages[room_id].append(record)
        return jsonify(record), 201

    return jsonify(messages.get(room_id, []))


@chat_bp.route('/chat')
def chat_ui():
    """Render the chat UI."""
    return render_template('chat/index.html')

from flask import Blueprint, jsonify

from ..models import ChatRoom

bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@bp.get('/rooms')
def list_rooms():
    rooms = ChatRoom.query.all()
    return jsonify([{'id': r.id, 'name': r.name} for r in rooms])
