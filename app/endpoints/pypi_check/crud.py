# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from loguru import logger

from com_lib import crud_ops
from com_lib.db_setup import libraries
from com_lib.db_setup import requirements
import settings
import random
import time


async def store_in_data(store_values: dict):

    query = requirements.insert()
    await crud_ops.execute_one_db(query=query, values=store_values)
    rgi = store_values["request_group_id"]
    logger.info(f"Created {rgi}")
    # return request_group_id


async def store_lib_request(json_data: dict, request_group_id: str):

    if settings.DEMO_DATA_CREATE == True:
        negative_days = random.randint(1, 900)
        now = datetime.today() - timedelta(days=negative_days)
    else:
        now = datetime.now()

    query = libraries.insert()
    values = {
        "id": str(uuid.uuid4()),
        "request_group_id": request_group_id,
        "library": json_data["library"],
        "currentVersion": json_data["currentVersion"],
        "newVersion": json_data["newVersion"],
        "dated_created": now,
    }
    await crud_ops.execute_one_db(query=query, values=values)
    logger.info(f"created request_group_id: {request_group_id}")


async def store_lib_data(request_group_id: str, json_data: dict):

    bulk_data: list = []
    for j in json_data:
        lib_update: dict = {
            "id": str(uuid.uuid4()),
            "request_group_id": request_group_id,
            "library": j["library"],
            "currentVersion": j["currentVersion"],
            "newVersion": j["newVersion"],
            "dated_created": datetime.now(),
        }
        bulk_data.append(lib_update)

    query = libraries.insert()
    values = bulk_data
    await crud_ops.execute_many_db(query=query, values=values)
    logger.info(f"created request_group_id: {request_group_id}")
    return request_group_id


async def get_request_group_id(request_group_id: str):

    query = requirements.select().where(
        requirements.c.request_group_id == request_group_id
    )
    result = await crud_ops.fetch_one_db(query=query)
    logger.debug(str(result))
    logger.info(f"returning results for {request_group_id}")
    return result
