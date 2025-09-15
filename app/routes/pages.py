from flask import Blueprint, render_template

from ..models import Page


pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/pages/<slug>')
def show_page(slug: str):
    page = Page.query.filter_by(slug=slug).first_or_404()
    return render_template('pages/show.html', page=page)
