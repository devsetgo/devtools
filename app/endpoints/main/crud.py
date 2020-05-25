# -*- coding: utf-8 -*-
from com_lib import crud_ops
from com_lib.db_setup import requirements, libraries
import uuid
from datetime import datetime
from starlette.background import BackgroundTask
from loguru import logger


async def get_data():

    query = libraries.select()
    result = await crud_ops.fetch_all_db(query=query)
    logger.critical(result)
    return result
