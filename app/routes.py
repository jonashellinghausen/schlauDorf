import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from .helpers import allowed_file
from .extensions import limiter

api_bp = Blueprint('api', __name__)


@api_bp.route('/upload', methods=['POST'])
@limiter.limit('10/minute')
def upload_file():
    """Upload a file if it has an allowed extension."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    filename = secure_filename(file.filename)
    upload_path = os.path.join('/tmp', filename)
    file.save(upload_path)
    return jsonify({'filename': filename}), 201


@api_bp.route('/ping')
@limiter.limit('5/minute')
def ping():
    """Simple health check route."""
    return jsonify({'message': 'pong'})
