from flask_socketio import join_room as socket_join_room, emit
from .extensions import socketio, db
from .models import ChatMessage


@socketio.on('join_room')
def handle_join_room(data):
    room = data.get('room')
    if room is not None:
        socket_join_room(room)


@socketio.on('send_message')
def handle_send_message(data):
    room_id = data.get('room_id')
    user_id = data.get('user_id')
    message = data.get('message')
    if None in (room_id, user_id, message):
        return
    chat_message = ChatMessage(room_id=room_id, user_id=user_id, message=message)
    db.session.add(chat_message)
    db.session.commit()
    emit('receive_message', {
        'id': chat_message.id,
        'room_id': room_id,
        'user_id': user_id,
        'message': message,
        'created_at': chat_message.created_at.isoformat()
    }, room=room_id)
