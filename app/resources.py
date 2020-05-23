# -*- coding: utf-8 -*-
from loguru import logger
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from com_lib import db_setup
from com_lib.db_setup import create_db
from com_lib.logging_config import config_logging

# templates and static files
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="statics")


def init_app():

    config_logging()
    logger.info("Initiating application")
    create_db()
    logger.info("Initiating database")


async def startup():

    logger.info("starting up services")
    await db_setup.connect_db()


async def shutdown():

    logger.info("shutting down services")
    await db_setup.disconnect_db()
