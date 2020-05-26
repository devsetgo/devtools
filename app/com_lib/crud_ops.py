# -*- coding: utf-8 -*-
"""
database simple functions. Pass query and where needed values and get result back
"""
from typing import Any
from typing import Dict
from typing import List

from loguru import logger
from sqlalchemy.sql import text

from com_lib.db_setup import database


async def fetch_one_db(query):
    """
    query = table.select().where(table.c.column == value)
    """
    result = await database.fetch_one(query)
    logger.debug(str(result))
    return result


async def fetch_all_db(query):
    """
    query = table.select()
    query = table.select().where(table.c.column == value)
    """
    result = await database.fetch_all(query)
    logger.debug(str(result))
    return result


async def execute_one_db(query, values: dict):
    """
    query = table.insert()
    query = table.update().where(table.c.column == value)
    values = {"column_1": "value","column_1": "value",}
    """
    result = await database.execute(query, values)
    logger.debug(str(result))
    return result


async def execute_many_db(query, values: List[Any]):
    """
    query = table.insert()
    query = table.update().where(table.c.column == value)
    values = [{"column_1": "value","column_1": "value"},{"column_1": "value","column_1": "value"}]
    """
    result = await database.execute_many(query, values)
    logger.debug(str(result))
    return result
