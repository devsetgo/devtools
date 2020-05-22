# -*- coding: utf-8 -*-
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from endpoints.bots import crud as bot_crud
from resources import templates


async def pypi_page(request):

    bots_all = await bot_crud.get_active_bots()
    template = f"/visitor/index.html"
    context = {"request": request, "bots_all": bots_all}
    logger.info(f"page accessed: /twitter_bots")
    return templates.TemplateResponse(template, context)


async def about_page(request):

    template = f"about.html"
    context = {"request": request}
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)


async def twitter_bots(request):

    bots_all = await bot_crud.get_active_bots()
    template = f"/visitor/index.html"
    context = {"request": request, "bots_all": bots_all}
    logger.info(f"page accessed: /twitter_bots")
    return templates.TemplateResponse(template, context)
