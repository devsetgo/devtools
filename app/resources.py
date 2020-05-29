# -*- coding: utf-8 -*-
from loguru import logger
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from com_lib import db_setup
from com_lib.db_setup import create_db
from com_lib.demo_data import make_a_lot_of_calls
import settings
from endpoints.main.crud import get_data

# templates and static files
templates = Jinja2Templates(directory="templates")
statics = StaticFiles(directory="statics")


async def startup():

    logger.info("starting up services")
    await db_setup.connect_db()

    if settings.DEMO_DATA_CREATE == "True":
        logger.warning("Checking data history")
        data = await get_data()
        if len(data) == 0:
            logger.warning("Creation of Demo Data")
            await make_a_lot_of_calls()
            logger.warning("Completion of Demo Data")
        else:
            logger.warning(
                "Exiting Data in the database, please set DEMO_DATA_CREATE to False"
            )


async def shutdown():

    logger.info("shutting down services")
    await db_setup.disconnect_db()


def init_app():

    # config_log()
    # logger.info("Initiating application")
    create_db()
    logger.info("Initiating database")
