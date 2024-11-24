from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import events_controller
from my_project.auth.domain import Events

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.get('')
def get_all_events() -> Response:
    events = events_controller.find_all()
    events_dto = [event.put_into_dto() for event in events]
    return make_response(jsonify(events_dto), HTTPStatus.OK)

@events_bp.post('')
def create_event() -> Response:
    content = request.get_json()
    event = Events.create_from_dto(content)
    events_controller.create_event(event)
    return make_response(jsonify(event.put_into_dto()), HTTPStatus.CREATED)

@events_bp.get('/<int:event_id>')
def get_event(event_id: int) -> Response:
    event = events_controller.find_by_id(event_id)
    if event:
        return make_response(jsonify(event.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Event not found"}), HTTPStatus.NOT_FOUND)

@events_bp.put('/<int:event_id>')
def update_event(event_id: int) -> Response:
    content = request.get_json()
    event = Events.create_from_dto(content)
    events_controller.update_event(event_id, event)
    return make_response("Event updated", HTTPStatus.OK)

@events_bp.delete('/<int:event_id>')
def delete_event(event_id: int) -> Response:
    events_controller.delete_event(event_id)
    return make_response("Event deleted", HTTPStatus.NO_CONTENT)
