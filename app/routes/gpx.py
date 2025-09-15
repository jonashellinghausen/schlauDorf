"""Routes for working with GPX tracks."""

from __future__ import annotations

import os

from flask import Blueprint, current_app, jsonify, request, send_file
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import GPXTrack
from ..utils.gpx import process_gpx_file

bp = Blueprint("gpx", __name__, url_prefix="/api/gpx")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ALLOWED_EXTENSIONS = {"gpx"}


def allowed_file(filename: str) -> bool:
    """Return ``True`` if the filename has an allowed extension."""

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@bp.get("/tracks")
def list_tracks():
    """Return public tracks."""

    tracks = GPXTrack.query.filter_by(is_public=True).all()
    return jsonify([{ "id": t.id, "name": t.name } for t in tracks])


@bp.post("/upload")
def upload_track():
    """Upload a GPX file and create a ``GPXTrack`` entry."""

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    name = request.form.get("name", file.filename)
    description = request.form.get("description")

    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "app/static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file.filename)

    # Process the GPX content before saving the file
    geometry, distance_km, elevation_gain = process_gpx_file(file.stream)
    file.stream.seek(0)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    track = GPXTrack(
        name=name,
        description=description,
        filename=filename,
        track_data=f"SRID=4326;{geometry}",
        distance_km=distance_km,
        elevation_gain_m=elevation_gain,
    )

    db.session.add(track)
    db.session.commit()

    return jsonify({"id": track.id, "name": track.name}), 201


@bp.get("/<int:track_id>/download")
def download_track(track_id: int):
    """Download the original GPX file for a track."""

    track = GPXTrack.query.get_or_404(track_id)
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "app/static/uploads")
    file_path = os.path.join(upload_folder, track.filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True, download_name=track.filename)
