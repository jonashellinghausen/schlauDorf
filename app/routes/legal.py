"""Routes for legal information pages."""

from flask import Blueprint, render_template

bp = Blueprint('legal', __name__)


@bp.route('/impressum')
def impressum():
    """Display the Impressum page."""
    return render_template('legal/impressum.html')


@bp.route('/datenschutz')
def datenschutz():
    """Display the Datenschutzerklärung page."""
    return render_template('legal/datenschutz.html')
