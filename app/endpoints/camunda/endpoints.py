# -*- coding: utf-8 -*-
"""
Application health endpoints
"""
from loguru import logger
from starlette.responses import JSONResponse
from resources import templates
import settings
import httpx
from endpoints.camunda.rest_calls import (
    task_data,
    task_comment,
    task_variables,
    task_rendered_form,
)

base_endpoint: str = "camunda"

base_url: str = settings.CAM_ENGINE_URL


async def task_list(request):
    """
    Task List
    """
    task_url = f"{base_url}/task"

    try:
        r = httpx.get(task_url)
        r.raise_for_status()
        tasks = r.json()
        status_code = r.status_code
        logger.info(f"API status cide of {status_code}")
    except httpx.RequestError as exc:
        logger.info(f"API Call Error {exc}")
        status_code = "Error"
        tasks = []

    data = {"status": status_code, "tasks": tasks}

    template: str = f"{base_endpoint}/task_list.html"
    context: dict = {"request": request, "data": data}
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)


async def task_item(request):
    """
    Task Item
    """
    task_id = request.path_params["page"]
    logger.info(f"fetching data for ID: {task_id}")
    task_url = f"{base_url}/task/{task_id}"
    # task_id,task_comment,task_variables
    task = await task_data(id=task_id)
    logger.debug(task)
    comment = await task_comment(id=task_id)
    logger.debug(comment)
    rendered_form = await task_rendered_form(id=task_id)

    template: str = f"{base_endpoint}/task_item.html"
    context: dict = {
        "request": request,
        "task": task,
        "taskId": task_id,
        "comment": comment,
        "rendered_form": rendered_form,
    }
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)
