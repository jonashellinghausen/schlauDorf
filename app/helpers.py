from flask import current_app


def allowed_file(filename: str) -> bool:
    """Check if a filename has an allowed extension.

    The list of allowed extensions is loaded from the application's
    ``ALLOWED_EXTENSIONS`` configuration variable.
    """
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', set())
    return ext in allowed
