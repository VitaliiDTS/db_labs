from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import event_types_controller
from my_project.auth.domain import EventTypes

event_types_bp = Blueprint('event_types', __name__, url_prefix='/event-types')

@event_types_bp.get('')
def get_all_event_types() -> Response:
    """
    Отримує всі типи подій з бази даних.
    """
    event_types = event_types_controller.find_all()
    event_types_dto = [event_type.put_into_dto() for event_type in event_types]
    return make_response(jsonify(event_types_dto), HTTPStatus.OK)

@event_types_bp.post('')
def create_event_type() -> Response:
    """
    Створює новий тип події в базі даних.
    """
    content = request.get_json()
    event_type = EventTypes.create_from_dto(content)
    event_types_controller.create_event_type(event_type)
    return make_response(jsonify(event_type.put_into_dto()), HTTPStatus.CREATED)

@event_types_bp.get('/<int:event_type_id>')
def get_event_type(event_type_id: int) -> Response:
    """
    Отримує тип події за ID.

    """
    event_type = event_types_controller.find_by_id(event_type_id)
    if event_type:
        return make_response(jsonify(event_type.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Event type not found"}), HTTPStatus.NOT_FOUND)

@event_types_bp.put('/<int:event_type_id>')
def update_event_type(event_type_id: int) -> Response:
    """
    Оновлює тип події за ID.

    """
    content = request.get_json()
    event_type = EventTypes.create_from_dto(content)
    event_types_controller.update_event_type(event_type_id, event_type)
    return make_response("Event type updated", HTTPStatus.OK)

@event_types_bp.delete('/<int:event_type_id>')
def delete_event_type(event_type_id: int) -> Response:
    """
    Видаляє тип події за ID.

    """
    event_types_controller.delete_event_type(event_type_id)
    return make_response("Event type deleted", HTTPStatus.NO_CONTENT)

@event_types_bp.get('/name/<string:name>')
def get_event_types_by_name(name: str) -> Response:
    """
    Отримує типи подій за назвою.

    """
    event_types = event_types_controller.get_event_types_by_name(name)
    return make_response(jsonify([event_type.put_into_dto() for event_type in event_types]), HTTPStatus.OK)
