from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/chat/rooms/<int:room_id>')
def chat_room(room_id: int):
    return render_template('chat/room.html', room_id=room_id)
