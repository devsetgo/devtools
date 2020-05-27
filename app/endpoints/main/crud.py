# -*- coding: utf-8 -*-
import collections

from loguru import logger

from com_lib import crud_ops
from com_lib.db_setup import libraries


async def get_data():

    query = libraries.select()
    result = await crud_ops.fetch_all_db(query=query)
    # logger.critical(str(result))
    return result


async def process_by_month(data: dict) -> dict:
    """
    Count by month of libraries checked
    """
    month_list = []
    for d in data:
        date_item = d["dated_created"]
        month = date_item.strftime("%b")
        month_list.append(month)

    count_obj = collections.Counter(month_list)
    result: dict = dict(count_obj)
    logger.debug(result)
    return result


async def sum_lib(data: dict):

    result: int = sum(data.values())
    logger.debug(result)
    return result


async def process_by_lib(data: dict) -> dict:
    """
    Count by number of versions of library & how often checked
    """
    library_list = []
    for d in data:
        library_list.append(d["library"])
    result: dict = dict(collections.Counter(library_list))
    logger.debug(f"by library: {result}")
    return result


async def sum_lib_count(data: dict):

    result: int = sum(data.values())
    logger.debug(result)
    return result
