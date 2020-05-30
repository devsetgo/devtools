# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""
import os
import secrets

from loguru import logger
from starlette.config import Config

# get environment variables
config = Config(".env")
USE_ENV = config("USE_ENV", default="docker")

CSRF_SECRET = secrets.token_urlsafe(64)
SECRET_KEY = secrets.token_hex(64)
INVALID_CHARACTER_LIST: list = [
    " ",
    ";",
    "<",
    ">",
    "/",
    "\\",
    "{",
    "}",
    "[",
    "]",
    "+",
    "=",
    "?",
    "&",
    "," ":",
    "'",
    ".",
    '"',
    "`",
]


# Application information
if USE_ENV.lower() == "dotenv":
    logger.info("external configuration is for use with {USE_ENV.lower()}")
    # dotenv variables
    APP_VERSION = config("APP_VERSION", default="1.0.0")
    # Application Configurations
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI", default="sqlite:///sqlite_db/starlette_ui.db"
    )
    # set release environment settings
    RELEASE_ENV = config("RELEASE_ENV", default="prd")
    # Safety check to prevent debug mode or mocking in production
    if RELEASE_ENV == "prd":
        DEBUG = False
        DEMO_DATA_CREATE = False
    else:
        DEBUG = config("DEBUG", default=False)
        DEMO_DATA_CREATE = config("DEMO_DATA_CREATE", default="False")

    # Demo data
    DEMO_DATA_LOOPS = config("DEMO_DATA_LOOPS", default=0)

    # Loguru settings
    LOGURU_RETENTION = config("LOGURU_RETENTION", default="10 days")
    LOGURU_ROTATION = config("LOGURU_ROTATION", default="10 MB")
    LOGURU_LOGGING_LEVEL = config("LOGURU_LOGGING_LEVEL", default="WARNING")


else:
    logger.info(f"external configuration is for use with {USE_ENV.lower()}")
    # docker variables
    APP_VERSION = os.environ["APP_VERSION"]
    # Application Configurations
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    # set release environment settings
    RELEASE_ENV = os.environ["RELEASE_ENV"]
    # Safety check to prevent debug mode or mocking in production
    if RELEASE_ENV == "prd":
        DEBUG = False
        DEMO_DATA_CREATE = False
    else:
        DEBUG = bool(os.environ["DEBUG"])
        DEMO_DATA_CREATE_value = os.environ["DEMO_DATA_CREATE"]

    # Demo data
    DEMO_DATA_LOOPS = os.environ["DEMO_DATA_LOOPS"]
    # Loguru settings
    LOGURU_RETENTION = os.environ["LOGURU_RETENTION"]
    LOGURU_ROTATION = os.environ["LOGURU_ROTATION"]
    LOGURU_LOGGING_LEVEL = os.environ["LOGURU_LOGGING_LEVEL"]
