from flask import render_template

from . import bp


@bp.route('/maps')
def maps_index():
    """Render the map view."""
    return render_template('maps/index.html')
