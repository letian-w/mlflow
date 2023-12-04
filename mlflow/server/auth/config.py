import os
import configparser
from pathlib import Path
from typing import NamedTuple

from mlflow.environment_variables import MLFLOW_AUTH_CONFIG_PATH


class AuthConfig(NamedTuple):
    default_permission: str
    database_uri: str
    admin_username: str
    admin_password: str
    authorization_function: str


def _get_auth_config_path() -> str:
    return (
        MLFLOW_AUTH_CONFIG_PATH.get() or Path(__file__).parent.joinpath("basic_auth.ini").resolve()
    )


def read_auth_config() -> AuthConfig:
    config_path = _get_auth_config_path()
    config = configparser.ConfigParser()
    config.read(config_path)
    return AuthConfig(
        default_permission=os.getenv(
            "MLFLOW_AUTH_DEFAULT_PERMISSION",
            config["mlflow"]["default_permission"]
        ),
        database_uri=os.getenv(
            "MLFLOW_AUTH_DATABASE_URI",
            config["mlflow"]["database_uri"]
        ),
        admin_username=os.getenv(
            "MLFLOW_AUTH_ADMIN_USERNAME",
            config["mlflow"]["admin_username"]
        ),
        admin_password=os.getenv(
            "MLFLOW_AUTH_ADMIN_PASSWORD",
            config["mlflow"]["admin_password"]
        ),
        authorization_function=os.getenv(
            "MLFLOW_AUTH_AUTHORIZATION_FUNCTION",
            config["mlflow"].get(
                "authorization_function", "mlflow.server.auth:authenticate_request_basic_auth"
            )
        ),
    )
