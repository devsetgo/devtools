# -*- coding: utf-8 -*-
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from endpoints.bots import crud as bot_crud
from resources import templates


async def homepage(request):

    if "username" not in request.session:
        return RedirectResponse(url=f"/twitter-bots", status_code=303)

    return RedirectResponse(url=f"/bots/", status_code=303)


async def homepage_page(request):

    try:
        html_page = request.path_params["page"]
        template = f"{html_page}.html"
        context = {"request": request}
        logger.info(f"page accessed: {template}")
        return templates.TemplateResponse(template, context)

    except Exception as e:
        logger.critical(
            f"Error: Page accessed: /{html_page} , but HTML page {e} does not exist"
        )
        raise HTTPException(404, detail="page note found")


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
