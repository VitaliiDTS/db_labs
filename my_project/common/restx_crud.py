from __future__ import annotations
from typing import Callable, Any, Optional, Dict, List

from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import NotFound, BadRequest

def _to_dto(obj: Any) -> Dict[str, Any]:
    if obj is None:
        raise NotFound("Object not found")
    if hasattr(obj, "put_into_dto") and callable(obj.put_into_dto):
        return obj.put_into_dto()
    raise BadRequest("Model has no put_into_dto()")

def _to_dtos(items: List[Any]) -> List[Dict[str, Any]]:
    return [_to_dto(i) for i in items]

def make_crud_namespace(
    *,
    name: str,
    path: str,
    model_cls: type,
    list_fn: Optional[Callable[[], List[Any]]] = None,
    get_fn: Optional[Callable[[int], Any]] = None,
    create_fn: Optional[Callable[[Any], None]] = None,
    update_fn: Optional[Callable[[int, Any], None]] = None,
    delete_fn: Optional[Callable[[int], None]] = None,
) -> Namespace:

    ns = Namespace(name, description=f"{name} CRUD", path=path)


    dto = ns.model(f"{name}_dto", {
        "id": fields.Integer(required=False, description="ID"),
    })


    coll_attrs = {}

    if list_fn:
        def get(self):
            return _to_dtos(list_fn()), 200
        coll_attrs["get"] = get

    if create_fn:
        def post(self):
            data = request.get_json(force=True, silent=True) or {}
            try:
                obj = model_cls.create_from_dto(data)
            except Exception as e:
                raise BadRequest(f"Bad payload: {e}")
            create_fn(obj)
            return _to_dto(obj), 201
        coll_attrs["post"] = post

    if not coll_attrs:

        pass

    Coll = type("Collection", (Resource,), coll_attrs)
    ns.add_resource(Coll, "")


    item_attrs = {}

    if get_fn:
        def get(self, item_id: int):
            return _to_dto(get_fn(item_id)), 200
        item_attrs["get"] = get

    if update_fn:
        def put(self, item_id: int):
            data = request.get_json(force=True, silent=True) or {}
            try:
                obj = model_cls.create_from_dto(data)
            except Exception as e:
                raise BadRequest(f"Bad payload: {e}")
            update_fn(item_id, obj)

            return _to_dto(obj), 200
        item_attrs["put"] = put

    if delete_fn:
        def delete(self, item_id: int):
            delete_fn(item_id)
            return "", 204
        item_attrs["delete"] = delete

    Item = type("Item", (Resource,), item_attrs)
    ns.add_resource(Item, "/<int:item_id>")

    return ns
