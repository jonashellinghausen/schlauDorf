from flask import Blueprint, render_template

from ..models import News, Event

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/news/')
def news_list():
    news = (
        News.query.filter_by(is_published=True)
        .order_by(News.created_at.desc())
        .all()
    )
    return render_template('news/list.html', news=news)


@bp.route('/events/')
def events_list():
    events = Event.query.order_by(Event.start_date.asc()).all()
    return render_template('events/list.html', events=events)


@bp.route('/chat/rooms/<int:room_id>')
def chat_room(room_id: int):
    return render_template('chat/room.html', room_id=room_id)
