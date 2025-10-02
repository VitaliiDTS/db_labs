from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import payments_controller
from my_project.auth.domain import Payments

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


@payments_bp.get('')
def get_all_payments() -> Response:

    payments = payments_controller.get_all_payments()
    payments_dto = [payment.put_into_dto() for payment in payments]
    return make_response(jsonify(payments_dto), HTTPStatus.OK)


@payments_bp.post('')
def create_payment() -> Response:

    content = request.get_json()
    payment = Payments.create_from_dto(content)
    payments_controller.create_payment(payment)
    return make_response(jsonify(payment.put_into_dto()), HTTPStatus.CREATED)


@payments_bp.get('/statistic/<string:operation>')
def get_amount_statistic(operation: str) -> Response:

    if operation not in ['Max', 'Min', 'Sum', 'Avg']:
        return make_response({"error": "Invalid operation"}, HTTPStatus.BAD_REQUEST)

    statistic_value = payments_controller.get_amount_statistic(operation)
    return make_response(jsonify({"operation": operation, "result": statistic_value}), HTTPStatus.OK)
