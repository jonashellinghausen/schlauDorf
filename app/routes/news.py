from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring

from flask import Blueprint, Response, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from .. import db
from ..models import News


class NewsForm(FlaskForm):
    """Form for creating and updating news."""

    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    category = StringField('Category')
    image_filename = StringField('Image Filename')
    submit = SubmitField('Submit')


news_bp = Blueprint('news', __name__)


@news_bp.route('/news/')
def index():
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('news/index.html', news_list=news_list)


@news_bp.route('/news/<int:news_id>')
def detail(news_id):
    news_item = News.query.get_or_404(news_id)
    return render_template('news/detail.html', news=news_item)


@news_bp.route('/news/create', methods=['GET', 'POST'])
def create():
    form = NewsForm()
    if form.validate_on_submit():
        news_item = News(
            title=form.title.data,
            body=form.body.data,
            category=form.category.data,
            image_filename=form.image_filename.data,
            created_at=datetime.utcnow(),
        )
        db.session.add(news_item)
        db.session.commit()
        return redirect(url_for('news.detail', news_id=news_item.id))
    return render_template('news/form.html', form=form)


@news_bp.route('/news/<int:news_id>/edit', methods=['GET', 'POST'])
def edit(news_id):
    news_item = News.query.get_or_404(news_id)
    form = NewsForm(obj=news_item)
    if form.validate_on_submit():
        form.populate_obj(news_item)
        db.session.commit()
        return redirect(url_for('news.detail', news_id=news_item.id))
    return render_template('news/form.html', form=form)


@news_bp.route('/news/<int:news_id>/delete', methods=['POST'])
def delete(news_id):
    news_item = News.query.get_or_404(news_id)
    db.session.delete(news_item)
    db.session.commit()
    return redirect(url_for('news.index'))


@news_bp.route('/api/news/rss.xml')
def rss():
    """Return RSS feed of news items."""
    items = News.query.order_by(News.created_at.desc()).all()

    root = Element('rss', version='2.0')
    channel = SubElement(root, 'channel')
    SubElement(channel, 'title').text = 'News Feed'
    SubElement(channel, 'link').text = url_for('news.index', _external=True)
    SubElement(channel, 'description').text = 'Latest news items'

    for item in items:
        el = SubElement(channel, 'item')
        SubElement(el, 'title').text = item.title
        SubElement(el, 'description').text = item.body
        SubElement(el, 'link').text = url_for('news.detail', news_id=item.id, _external=True)
        if item.created_at:
            SubElement(el, 'pubDate').text = item.created_at.strftime(
                '%a, %d %b %Y %H:%M:%S GMT'
            )

    xml_str = tostring(root, encoding='utf-8')
    return Response(xml_str, mimetype='application/rss+xml')
