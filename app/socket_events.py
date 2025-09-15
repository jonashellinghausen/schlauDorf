from flask import request
from flask_socketio import join_room, emit

from .storage import messages


def init_socketio(socketio):
    @socketio.on('join_room')
    def handle_join_room(data):
        """Handle a user joining a chat room."""
        room = data.get('room')
        username = data.get('username', 'Anonymous')
        join_room(room)
        emit('status', {'msg': f"{username} has entered the room."}, room=room)

    @socketio.on('send_message')
    def handle_send_message(data):
        """Broadcast a message to all users in the room."""
        room = data.get('room')
        msg = data.get('message', '')
        username = data.get('username', 'Anonymous')
        if not room:
            return
        record = {'username': username, 'message': msg}
        messages[room].append(record)
        emit('receive_message', record, room=room)
