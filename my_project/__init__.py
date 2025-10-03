import os
import json
import secrets
from http import HTTPStatus
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

from my_project.auth.route import register_routes


SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
DB_SECRET_NAME_ENV = "DB_SECRET_NAME"

db = SQLAlchemy()
todos = {}
_secret_cache: Optional[dict] = None



def _fetch_secret_dict(secret_name: str) -> Optional[dict]:

    global _secret_cache
    if _secret_cache is not None:
        return _secret_cache
    try:
        client = boto3.client("secretsmanager", region_name=AWS_REGION)
        resp = client.get_secret_value(SecretId=secret_name)
        payload = resp.get("SecretString") or resp.get("SecretBinary")
        if not payload:
            return None
        data = json.loads(payload) if isinstance(payload, str) else json.loads(payload.decode("utf-8"))
        _secret_cache = data
        return data
    except (BotoCoreError, ClientError, json.JSONDecodeError):
        return None


def _build_sqlalchemy_uri_from_secret(data: dict) -> str:

    user = data["username"]
    pwd = data["password"]
    host = data["host"]
    port = data.get("port", 3306)
    dbname = data["database"]
    drv = data.get("driver", "mysqldb")  # mysqlclient -> mysqldb; PyMySQL -> pymysql
    return f"mysql+{drv}://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8mb4"




def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:

    _process_input_config(app_config, additional_config)

    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config.update(app_config)

    _init_db(app)
    register_routes(app)
    _init_swagger(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app



def _pick(controller, *names):

    for n in names:
        fn = getattr(controller, n, None)
        if callable(fn):
            return fn
    raise AttributeError(f"{controller} has none of {names}")


def _init_swagger(app: Flask) -> None:
    api = Api(
        app,
        title="VItalik Dats backend",
        description="animators db backend",
        doc="/docs",
    )

    from my_project.common.restx_crud import make_crud_namespace
    from my_project.auth.domain import (
        Animators, Agencies, Events, EventTypes, Payments, AnimatorAgencyContract
    )


    from my_project.auth.controller import (
        animators_controller,
        agencies_controller,
        events_controller,
        event_types_controller,
        payments_controller,
        animator_agency_contract_controller,
    )


    api.add_namespace(make_crud_namespace(
        name="animators", path="/animators", model_cls=Animators,
        list_fn=_pick(animators_controller, "find_all", "get_all_animators", "get_all"),
        get_fn=_pick(animators_controller, "find_by_id", "get_animator_by_id", "get_by_id"),
        create_fn=_pick(animators_controller, "create_animator", "create"),
        update_fn=_pick(animators_controller, "update_animator", "update"),
        #delete_fn=_pick(animators_controller, "delete_animator", "delete"),
    ))


    api.add_namespace(make_crud_namespace(
        name="agencies", path="/agencies", model_cls=Agencies,
        list_fn=_pick(agencies_controller, "find_all", "get_all_agencies", "get_all"),
        get_fn=_pick(agencies_controller, "find_by_id", "get_agency_by_id", "get_by_id"),
        create_fn=_pick(agencies_controller, "create_agency", "create"),
        update_fn=_pick(agencies_controller, "update_agency", "update"),
        delete_fn=_pick(agencies_controller, "delete_agency", "delete"),
    ))


    api.add_namespace(make_crud_namespace(
        name="event_types", path="/event_types", model_cls=EventTypes,
        list_fn=_pick(event_types_controller, "find_all", "get_all_event_types", "get_all"),
        get_fn=_pick(event_types_controller, "find_by_id", "get_event_type_by_id", "get_by_id"),
        create_fn=_pick(event_types_controller, "create_event_type", "create"),
        update_fn=_pick(event_types_controller, "update_event_type", "update"),
        delete_fn=_pick(event_types_controller, "delete_event_type", "delete"),
    ))


    api.add_namespace(make_crud_namespace(
        name="events", path="/events", model_cls=Events,
        list_fn=_pick(events_controller, "find_all", "get_all_events", "get_all"),
        get_fn=_pick(events_controller, "find_by_id", "get_event_by_id", "get_by_id"),
        create_fn=_pick(events_controller, "create_event", "create"),
        update_fn=_pick(events_controller, "update_event", "update"),
        delete_fn=_pick(events_controller, "delete_event", "delete"),
    ))


    api.add_namespace(make_crud_namespace(
        name="payments", path="/payments", model_cls=Payments,
        list_fn=_pick(payments_controller, "get_all_payments", "find_all", "get_all"),
        get_fn=_pick(payments_controller, "get_payment_by_id", "find_by_id", "get_by_id"),
        create_fn=_pick(payments_controller, "create_payment", "create"),
        update_fn=_pick(payments_controller, "update_payment", "update"),
        delete_fn=_pick(payments_controller, "delete_payment", "delete"),
    ))


    api.add_namespace(make_crud_namespace(
        name="animator_agency_contracts", path="/animator_agency_contracts",
        model_cls=AnimatorAgencyContract,
        list_fn=_pick(animator_agency_contract_controller, "find_all", "get_all_contracts", "get_all"),
        get_fn=_pick(animator_agency_contract_controller, "find_by_id", "get_contract_by_id", "get_by_id"),
        create_fn=_pick(animator_agency_contract_controller, "create_contract", "create"),
        update_fn=_pick(animator_agency_contract_controller, "update_contract", "update"),
        delete_fn=_pick(animator_agency_contract_controller, "delete_contract", "delete"),
    ))



def _init_db(app: Flask) -> None:

    db.init_app(app)

    try:
        uri = app.config[SQLALCHEMY_DATABASE_URI]
        if not database_exists(uri):
            create_database(uri)
    except Exception as e:
        app.logger.warning(f"DB create check skipped: {e}")

    import my_project.auth.domain  # noqa: F401
    with app.app_context():
        db.create_all()



def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:


    env_url = os.getenv("DATABASE_URL")
    if env_url:
        app_config[SQLALCHEMY_DATABASE_URI] = env_url
        return


    secret_name = os.getenv(DB_SECRET_NAME_ENV, "lab/mysql")
    secret = _fetch_secret_dict(secret_name)
    if secret:
        app_config[SQLALCHEMY_DATABASE_URI] = _build_sqlalchemy_uri_from_secret(secret)
        return


    uri = app_config.get(SQLALCHEMY_DATABASE_URI, "")
    if "{" in uri:
        root_user = os.getenv(MYSQL_ROOT_USER, additional_config.get(MYSQL_ROOT_USER, "root"))
        root_password = os.getenv(MYSQL_ROOT_PASSWORD, additional_config.get(MYSQL_ROOT_PASSWORD, "root"))
        app_config[SQLALCHEMY_DATABASE_URI] = uri.format(root_user, root_password)
        return


    raise RuntimeError(
        "SQLALCHEMY_DATABASE_URI is not configured. "
        "Set DATABASE_URL env, or provide DB_SECRET_NAME secret, or a valid URI in YAML."
    )
