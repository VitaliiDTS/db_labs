from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import animator_agency_contract_controller
from my_project.auth.domain import AnimatorAgencyContract

animator_agens_contracts_bp = Blueprint('contracts', __name__, url_prefix='/contracts')

@animator_agens_contracts_bp.get('')
def get_all_contracts() -> Response:
    contracts = animator_agency_contract_controller.find_all()
    return make_response(jsonify([contract.put_into_dto() for contract in contracts]), HTTPStatus.OK)

@animator_agens_contracts_bp.post('')
def create_contract() -> Response:
    content = request.get_json()
    contract = AnimatorAgencyContract.create_from_dto(content)
    animator_agency_contract_controller.create_contract(contract)
    return make_response(jsonify(contract.put_into_dto()), HTTPStatus.CREATED)

@animator_agens_contracts_bp.get('/<int:contract_id>')
def get_contract(contract_id: int) -> Response:
    contract = animator_agency_contract_controller.find_by_id(contract_id)
    return make_response(jsonify(contract.put_into_dto()), HTTPStatus.OK)

@animator_agens_contracts_bp.put('/<int:contract_id>')
def update_contract(contract_id: int) -> Response:
    content = request.get_json()
    contract = AnimatorAgencyContract.create_from_dto(content)
    animator_agency_contract_controller.update_contract(contract_id, contract)
    return make_response(jsonify(contract.put_into_dto()), HTTPStatus.OK)

@animator_agens_contracts_bp.delete('/<int:contract_id>')
def delete_contract(contract_id: int) -> Response:
    animator_agency_contract_controller.delete_contract(contract_id)
    return make_response('', HTTPStatus.NO_CONTENT)
