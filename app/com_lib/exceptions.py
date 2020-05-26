# -*- coding: utf-8 -*-
from loguru import logger
from starlette.responses import RedirectResponse

from resources import templates


async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    logger.error("Unknown exception has occurred. Use debug mode to troubleshoot")
    raise RuntimeError("Oh no")


async def not_allowed(request, exc):
    """
    Return an HTTP 403 page.
    """
    if "username" not in request.session:
        logger.error(
            f"user page access without being logged in from {request.client.host}"
        )
        return RedirectResponse(url="/", status_code=303)

    template = "error/403.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=403)


async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    if "username" not in request.session:
        logger.error(
            f"user page access without being logged in from {request.client.host}"
        )
        return RedirectResponse(url="/", status_code=303)

    template = "error/404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    if "username" not in request.session:
        logger.error(
            f"user page access without being logged in from {request.client.host}"
        )
        return RedirectResponse(url="/", status_code=303)

    template = "error/500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)
