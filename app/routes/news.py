from flask import Blueprint, jsonify

from ..models import News

bp = Blueprint('news', __name__, url_prefix='/api/news')


@bp.get('/')
def list_news():
    """Return published news items as JSON."""
    items = News.query.filter_by(is_published=True).all()
    return jsonify([
        {
            'id': item.id,
            'title': item.title,
            'content': item.content,
        }
        for item in items
    ])
