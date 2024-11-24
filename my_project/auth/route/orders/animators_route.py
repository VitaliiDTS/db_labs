from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import animators_controller
from my_project.auth.domain import Animators

animators_bp = Blueprint('animators', __name__, url_prefix='/animators')

@animators_bp.get('')
def get_all_animators() -> Response:
    return make_response(jsonify([animator.put_into_dto() for animator in animators_controller.find_all()]), HTTPStatus.OK)

@animators_bp.post('')
def create_animator() -> Response:
    content = request.get_json()
    animator = Animators.create_from_dto(content)
    animators_controller.create_animator(animator)
    return make_response(jsonify(animator.put_into_dto()), HTTPStatus.CREATED)

@animators_bp.get('/<int:animator_id>')
def get_animator(animator_id: int) -> Response:
    animator = animators_controller.find_by_id(animator_id)
    return make_response(jsonify(animator.put_into_dto()), HTTPStatus.OK)

@animators_bp.get('/name/<string:name>')
def get_animators_by_name(name: str) -> Response:
    animators = animators_controller.get_animators_by_name(name)
    return make_response(jsonify([animator.put_into_dto() for animator in animators]), HTTPStatus.OK)

@animators_bp.get('/phone/<string:phone>')
def get_animators_by_phone(phone: str) -> Response:
    animators = animators_controller.get_animators_by_phone(phone)
    return make_response(jsonify([animator.put_into_dto() for animator in animators]), HTTPStatus.OK)
@animators_bp.put('/<int:animator_id>')
def update_animator(animator_id: int) -> Response:

    content = request.get_json()
    animator = Animators.create_from_dto(content)
    animators_controller.update_animator(animator_id, animator)
    return make_response(jsonify(animator.put_into_dto()), HTTPStatus.OK)

@animators_bp.delete('/<int:animator_id>')
def delete_animator(animator_id: int) -> Response:

    animators_controller.delete_animator(animator_id)
    return make_response('', HTTPStatus.NO_CONTENT)
