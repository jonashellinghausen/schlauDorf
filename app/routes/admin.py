from flask import Blueprint, render_template, request, redirect, url_for

from .. import db
from ..models import Page


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/pages')
def list_pages():
    pages = Page.query.all()
    return render_template('admin/pages/index.html', pages=pages)


@admin_bp.route('/pages/new', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        title = request.form['title']
        slug = request.form['slug']
        content = request.form['content']
        page = Page(title=title, slug=slug, content=content)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('admin.list_pages'))
    return render_template('admin/pages/create.html')


@admin_bp.route('/pages/<int:page_id>/edit', methods=['GET', 'POST'])
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)
    if request.method == 'POST':
        page.title = request.form['title']
        page.slug = request.form['slug']
        page.content = request.form['content']
        db.session.commit()
        return redirect(url_for('admin.list_pages'))
    return render_template('admin/pages/edit.html', page=page)


@admin_bp.route('/pages/<int:page_id>/delete', methods=['POST'])
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    return redirect(url_for('admin.list_pages'))
