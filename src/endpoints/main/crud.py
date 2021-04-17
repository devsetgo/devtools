# -*- coding: utf-8 -*-
import collections

from loguru import logger

from com_lib import crud_ops
from com_lib.db_setup import libraries, requirements


async def get_data():

    query = libraries.select()
    data = await crud_ops.fetch_all_db(query=query)

    lib_data_month = await process_by_month(data)
    lib_sum = await sum_lib(lib_data_month)
    library_data_count = await process_by_lib(data)
    lib_data_sum = await sum_lib_count(library_data_count)
    lib_new_ver = await lib_new_versions(data)

    result = {
        "lib_data_month": lib_data_month,
        "lib_sum": lib_sum,
        "library_data_count": library_data_count,
        "lib_data_sum": lib_data_sum,
        "lib_new_ver": lib_new_ver,
    }
    return result


async def lib_new_versions(data: dict):

    ver = []
    for d in data:

        lib_ver = f'{d["library"]}={d["newVersion"]}'
        if lib_ver not in ver:
            ver.append(lib_ver)
    result = len(ver)

    return result


async def process_by_month(data: dict) -> dict:
    """
    Count by month of libraries checked
    """
    result: dict = {}
    for d in data:
        date_item = d["dated_created"]
        ym = date_item.strftime("%Y-%m")
        if ym not in result:
            result[ym] = 1
        else:
            result[ym] += 1

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
    result: dict = dict(collections.Counter(library_list).most_common(25))
    logger.debug(f"by library: {result}")
    return result


async def sum_lib_count(data: dict):

    result: int = sum(data.values())
    logger.debug(result)
    return result


async def requests_data():

    query = requirements.select()
    data = await crud_ops.fetch_all_db(query=query)

    ips = []
    for d in data:
        if d["host_ip"] not in ips:
            ips.append(d["host_ip"])

    result = {"unique": len(ips), "fulfulled": len(data)}
    logger.debug(result)
    return result
