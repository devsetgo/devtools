# -*- coding: utf-8 -*-
"""
Application health endpoints
"""
from loguru import logger
import httpx
import settings

client = httpx.AsyncClient()

base_url: str = settings.CAM_ENGINE_URL


async def camunda_call(url):
    try:
        r = httpx.get(url)
        r.raise_for_status()
        data = r.json()
        status_code = r.status_code
        logger.info(f"API status cide of {status_code}")
    except httpx.RequestError as exc:
        logger.info(f"API Call Error {exc}")
        status_code = "Error"
        data = []

    result = {"status": status_code, "data": data}
    return result


async def task_data(id: str):

    task_url = f"{base_url}/task/{id}"
    result = await camunda_call(url=task_url)
    return result


async def task_comment(id: str):
    logger.critical(id)
    task_url = f"{base_url}/task/{id}/comment"
    result = await camunda_call(url=task_url)
    # r = httpx.get(task_url)
    # logger.critical("BOB")
    # if r.status_code == 200:
    #     result = r.json()
    # else:
    #     result = {"error": r.status_code}
    # logger.critical(result)
    return result

    # return result


async def task_variables(id: str):

    task_url = f"{base_url}/task/{id}/variables"
    result = await camunda_call(url=task_url)
    return result


async def task_rendered_form(id: str):

    url = f"{base_url}/task/{id}/rendered-form"

    r = await client.get(url)
    if r.status_code == 200:
        result = r.text
    else:
        result = "Error"
    return result
