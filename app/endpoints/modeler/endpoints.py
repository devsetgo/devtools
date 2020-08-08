# -*- coding: utf-8 -*-
"""
Application health endpoints
"""
from loguru import logger
from starlette.responses import JSONResponse
from resources import templates


base: str = "modeler_pages"

async def viewer_bpmn(request):
    """
    BPM Viewer Page
    """
    status_code = 200
    template = f"/{base}/viewer_bpmn.html"
    context = {"request": request}
    logger.info("page accessed: /modeler/bpmn/view")
    return templates.TemplateResponse(template, context, status_code=status_code)


async def modeler_bpmn(request):
    """
    BPM Viewer Page
    """
    status_code = 200
    template = f"/{base}/modeler_bpmn.html"
    context = {"request": request}
    logger.info("page accessed: /modeler/bpmn/view")
    return templates.TemplateResponse(template, context, status_code=status_code)
