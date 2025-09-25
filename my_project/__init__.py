"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""

import os
import json
import secrets
from http import HTTPStatus
from typing import Dict, Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import Flask
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

from my_project.auth.route import register_routes

# ---- constants & globals -----------------------------------------------------

SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
DB_SECRET_NAME_ENV = "DB_SECRET_NAME"          # напр. "lab/mysql"

db = SQLAlchemy()
todos = {}
_secret_cache: dict | None = None


# ---- secrets helpers ---------------------------------------------------------

def _fetch_secret_dict(secret_name: str) -> dict | None:
    """Get and cache secret JSON from AWS Secrets Manager."""
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
    """Compose SQLAlchemy URI from secret dict."""
    user = data["username"]
    pwd = data["password"]
    host = data["host"]
    port = data.get("port", 3306)
    dbname = data["database"]
    drv = data.get("driver", "mysqldb")  # mysqlclient -> mysqldb; PyMySQL -> pymysql
    return f"mysql+{drv}://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8mb4"


# ---- app factory -------------------------------------------------------------

def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    """
    Creates Flask application
    :param app_config: Flask configuration (from YAML)
    :param additional_config: extra config (from YAML)
    """
    _process_input_config(app_config, additional_config)

    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config = {**app.config, **app_config}

    _init_db(app)
    register_routes(app)
    _init_swagger(app)

    # health endpoint for checks/load balancer
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app


# ---- swagger demo (left as-is) ----------------------------------------------

def _init_swagger(app: Flask) -> None:
    restx_api = Api(app, title='VItalik Dats backend', description='animators db backend')

    @restx_api.route('/number/<string:todo_id>')
    class TodoSimple(Resource):
        @staticmethod
        def get(todo_id):
            return todos, 202

        @staticmethod
        def put(todo_id):
            todos[todo_id] = todo_id
            return todos, HTTPStatus.CREATED

        @staticmethod
        def post(todo_id):
            todos[todo_id] = {"task": f"New task with ID {todo_id}"}
            return todos[todo_id], HTTPStatus.CREATED

    @app.route("/hi")
    def hello_world():
        return todos, HTTPStatus.OK


# ---- db init ----------------------------------------------------------------

def _init_db(app: Flask) -> None:
    """Initializes DB with SQLAlchemy."""
    db.init_app(app)
    # На RDS create_database може бути заборонено: загортаємо обережно
    try:
        uri = app.config[SQLALCHEMY_DATABASE_URI]
        if not database_exists(uri):
            create_database(uri)
    except Exception as e:
        app.logger.warning(f"DB create check skipped: {e}")

    import my_project.auth.domain  # noqa: F401
    with app.app_context():
        db.create_all()


# ---- config processing -------------------------------------------------------

def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    """
    Finalize app_config[SQLALCHEMY_DATABASE_URI] with precedence:
      1) env: DATABASE_URL
      2) AWS Secrets Manager (DB_SECRET_NAME / default 'lab/mysql')
      3) YAML (and only format with root if URI has '{}' placeholders)
    """
    # 1) explicit env override
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        app_config[SQLALCHEMY_DATABASE_URI] = env_url
        return

    # 2) secrets manager
    secret_name = os.getenv(DB_SECRET_NAME_ENV, "lab/mysql")
    secret = _fetch_secret_dict(secret_name)
    if secret:
        app_config[SQLALCHEMY_DATABASE_URI] = _build_sqlalchemy_uri_from_secret(secret)
        return

    # 3) fallback to YAML (format only if placeholders exist)
    uri = app_config.get(SQLALCHEMY_DATABASE_URI, "")
    if "{" in uri:
        root_user = os.getenv(MYSQL_ROOT_USER, additional_config.get(MYSQL_ROOT_USER, "root"))
        root_password = os.getenv(MYSQL_ROOT_PASSWORD, additional_config.get(MYSQL_ROOT_PASSWORD, "root"))
        app_config[SQLALCHEMY_DATABASE_URI] = uri.format(root_user, root_password)
