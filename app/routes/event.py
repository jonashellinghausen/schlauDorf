from flask import (
    Blueprint,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from ..forms import EventForm


event_bp = Blueprint("event", __name__)

# In-memory storage for events
_events = []
_next_id = 1


def _get_event(event_id):
    return next((e for e in _events if e["id"] == event_id), None)


@event_bp.route("/events")
def list_events():
    """Display a list of events."""
    return render_template("events/list.html", events=_events)


@event_bp.route("/events/<int:event_id>")
def event_detail(event_id):
    """Display an event's details."""
    event = _get_event(event_id)
    if not event:
        abort(404)
    return render_template("events/detail.html", event=event)


@event_bp.route("/events/new", methods=["GET", "POST"])
def create_event():
    """Create a new event."""
    global _next_id
    form = EventForm()
    if form.validate_on_submit():
        event = {
            "id": _next_id,
            "title": form.title.data,
            "description": form.description.data,
        }
        _events.append(event)
        _next_id += 1
        return redirect(url_for("event.list_events"))
    return render_template("events/form.html", form=form)


@event_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    """Edit an existing event."""
    event = _get_event(event_id)
    if not event:
        abort(404)

    form = EventForm(data=event)
    if form.validate_on_submit():
        event["title"] = form.title.data
        event["description"] = form.description.data
        return redirect(url_for("event.event_detail", event_id=event_id))
    return render_template("events/form.html", form=form, event=event)


@event_bp.route("/events/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    """Delete an event."""
    event = _get_event(event_id)
    if not event:
        abort(404)
    _events.remove(event)
    return redirect(url_for("event.list_events"))


# REST API endpoints
@event_bp.route("/api/events", methods=["GET"])
def api_list_events():
    return jsonify(_events)


@event_bp.route("/api/events/<int:event_id>", methods=["GET"])
def api_get_event(event_id):
    event = _get_event(event_id)
    if not event:
        abort(404)
    return jsonify(event)


@event_bp.route("/api/events", methods=["POST"])
def api_create_event():
    global _next_id
    data = request.get_json() or {}
    event = {
        "id": _next_id,
        "title": data.get("title", ""),
        "description": data.get("description", ""),
    }
    _events.append(event)
    _next_id += 1
    return jsonify(event), 201


@event_bp.route("/api/events/<int:event_id>", methods=["PUT"])
def api_update_event(event_id):
    event = _get_event(event_id)
    if not event:
        abort(404)
    data = request.get_json() or {}
    event["title"] = data.get("title", event["title"])
    event["description"] = data.get("description", event["description"])
    return jsonify(event)


@event_bp.route("/api/events/<int:event_id>", methods=["DELETE"])
def api_delete_event(event_id):
    event = _get_event(event_id)
    if not event:
        abort(404)
    _events.remove(event)
    return "", 204
