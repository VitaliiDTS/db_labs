from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import agencies_controller
from my_project.auth.domain import Agencies  # Виправлено на правильний імпорт

agencies_bp = Blueprint('agencies', __name__, url_prefix='/agencies')

@agencies_bp.get('')
@agencies_bp.get('')
def get_all_agencies() -> Response:
    """
    Gets all agencies from the database.
    """
    agencies = agencies_controller.find_all()
    agencies_dto = [agency.put_into_dto() for agency in agencies]
    return make_response(jsonify(agencies_dto), HTTPStatus.OK)

@agencies_bp.post('')
def create_agency() -> Response:
    """
    Creates a new agency in the database.
    """
    content = request.get_json()
    agency = Agencies.create_from_dto(content)
    agencies_controller.create_agency(agency)
    return make_response(jsonify(agency.put_into_dto()), HTTPStatus.CREATED)

@agencies_bp.get('/<int:agency_id>')
def get_agency(agency_id: int) -> Response:
    """
    Gets agency by ID.
    """
    agency = agencies_controller.find_by_id(agency_id)
    if agency:
        return make_response(jsonify(agency.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Agency not found"}), HTTPStatus.NOT_FOUND)

@agencies_bp.put('/<int:agency_id>')
def update_agency(agency_id: int) -> Response:
    """
    Updates agency by ID.
    """
    content = request.get_json()
    agency = Agencies.create_from_dto(content)
    agencies_controller.update_agency(agency_id, agency)
    return make_response("Agency updated", HTTPStatus.OK)

@agencies_bp.delete('/<int:agency_id>')
def delete_agency(agency_id: int) -> Response:
    """
    Deletes agency by ID.
    """
    agencies_controller.delete_agency(agency_id)
    return make_response("Agency deleted", HTTPStatus.NO_CONTENT)

@agencies_bp.get('/name/<string:name>')
def get_agencies_by_name(name: str) -> Response:
    """
    Gets agencies by name.

    """
    agencies = agencies_controller.get_agencies_by_name(name)
    return make_response(jsonify([agency.put_into_dto() for agency in agencies]), HTTPStatus.OK)

@agencies_bp.get('/phone/<string:phone>')
def get_agencies_by_phone(phone: str) -> Response:
    """
    Gets agencies by phone.

    """
    agencies = agencies_controller.get_agencies_by_phone(phone)
    return make_response(jsonify([agency.put_into_dto() for agency in agencies]), HTTPStatus.OK)

@agencies_bp.post('/multiple/procedure')
def create_multiple_agencies_using_procedure() -> Response:
    """
    Створює 10 нових агентств у базі даних, викликаючи збережену процедуру.
    """
    agencies_controller.create_multiple_agencies_using_procedure()
    return make_response("10 agencies created successfully using procedure", HTTPStatus.CREATED)

@agencies_bp.post('/call-procedure')
def call_procedure() -> Response:
    """
    Викликає збережену процедуру для створення та вставки даних.
    """
    try:
        agencies_controller.call_create_and_insert_procedure()
        return make_response(jsonify({"message": "Procedure successfully executed"}), HTTPStatus.OK)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR)
