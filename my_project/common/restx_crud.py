from __future__ import annotations
from typing import Callable, Dict, Any, Optional, Type
from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from sqlalchemy import Integer, String, Float, Boolean, Date, DateTime, Text
from sqlalchemy.orm import DeclarativeMeta

_TYPE_MAP = {
    Integer: fields.Integer,
    String:  fields.String,
    Text:    fields.String,
    Float:   fields.Float,
    Boolean: fields.Boolean,
    Date:    fields.String,
    DateTime: fields.String,
}

def _build_restx_model_from_sqla(api: Namespace, model_cls: Type[DeclarativeMeta]) -> fields.Model:
    schema: Dict[str, Any] = {}
    for col in model_cls.__table__.columns:

        restx_type = None
        for sqla_type, restx in _TYPE_MAP.items():
            if isinstance(col.type, sqla_type):
                restx_type = restx
                break
        restx_type = restx_type or fields.String

        schema[col.name] = restx_type(
            readonly=col.primary_key is True,
            required=(not col.nullable and not col.primary_key)
        )
    return api.model(model_cls.__name__, schema)

def make_crud_namespace(
    name: str,
    path: str,
    model_cls: Type[DeclarativeMeta],
    *,
    list_fn: Callable[[], list],
    get_fn: Callable[[int], Any],
    create_fn: Callable[[Any], None],
    update_fn: Callable[[int, Any], None],
    delete_fn: Callable[[int], None],
) -> Namespace:

    api = Namespace(name, description=f"{name} CRUD", path=path)
    restx_model = _build_restx_model_from_sqla(api, model_cls)

    @api.route("")
    class Collection(Resource):
        @api.marshal_list_with(restx_model, code=HTTPStatus.OK)
        def get(self):
            items = list_fn()
            return [i.put_into_dto() for i in items]

        @api.expect(restx_model, validate=True)
        @api.marshal_with(restx_model, code=HTTPStatus.CREATED)
        def post(self):
            payload = request.get_json()
            obj = model_cls.create_from_dto(payload)
            create_fn(obj)
            return obj.put_into_dto(), HTTPStatus.CREATED

    @api.route("/<int:item_id>")
    @api.response(404, "Not found")
    class Item(Resource):
        @api.marshal_with(restx_model)
        def get(self, item_id: int):
            obj = get_fn(item_id)
            return obj.put_into_dto()

        @api.expect(restx_model, validate=True)
        @api.marshal_with(restx_model, code=HTTPStatus.OK)
        def put(self, item_id: int):
            payload = request.get_json()
            obj = model_cls.create_from_dto(payload)
            update_fn(item_id, obj)

            fresh = get_fn(item_id)
            return fresh.put_into_dto(), HTTPStatus.OK

        def delete(self, item_id: int):
            delete_fn(item_id)
            return "", HTTPStatus.NO_CONTENT

    return api
