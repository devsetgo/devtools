# -*- coding: utf-8 -*-
from loguru import logger
from starlette.responses import RedirectResponse

from endpoints.main import crud as lib_crud
from resources import templates


async def homepage(request):
    return RedirectResponse(url="/index", status_code=303)


async def about_page(request):

    template: str = "about.html"
    context: dict = {"request": request}
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)


@logger.catch
async def index(request):

    lib_data = await lib_crud.get_data()

    lib_data_month = await lib_crud.process_by_month(lib_data)
    lib_sum = await lib_crud.sum_lib(lib_data_month)
    library_data_count = await lib_crud.process_by_lib(lib_data)
    lib_data_sum = await lib_crud.sum_lib_count(library_data_count)

    data: dict = {
        "lib_data_month": lib_data_month,
        "lib_sum": lib_sum,
        "library_data_count": library_data_count,
        "lib_data_sum": lib_data_sum,
    }

    logger.critical(data)

    template: str = "index3.html"
    context = {"request": request, "data": data}
    logger.critical(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)
