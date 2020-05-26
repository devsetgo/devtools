# -*- coding: utf-8 -*-
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from endpoints.main import crud as lib_crud

from resources import templates


async def homepage(request):
    return RedirectResponse(url=f"/index", status_code=303)


# async def homepage_page(request):

#     try:
#         html_page = request.path_params["page"]
#         template = f"{html_page}.html"
#         context = {"request": request}
#         logger.info(f"page accessed: {template}")
#         return templates.TemplateResponse(template, context)

#     except Exception as e:
#         logger.critical(
#             f"Error: Page accessed: /{html_page} , but HTML page {e} does not exist"
#         )
#         raise HTTPException(404, detail="page note found")


async def about_page(request):

    template: str = f"about.html"
    context: dict = {"request": request}
    logger.info(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)


async def index(request):

    lib_data = await lib_crud.get_data()
    
    lib_data_month = await lib_crud.process_by_month(lib_data)
    lib_sum = await lib_crud.sum_lib(lib_data_month)
    library_data_count = await lib_crud.process_by_lib(lib_data)
    lib_data_sum = await lib_crud.sum_lib_count(library_data_count)
    
    data: dict ={"lib_data_month":lib_data_month,"lib_sum":lib_sum,"library_data_count":library_data_count,"lib_data_sum":lib_data_sum}
    
    logger.critical(data)

    template: str = f"index3.html"
    context: dict = {"request": request, "data":data}
    logger.critical(f"page accessed: /{template}")
    return templates.TemplateResponse(template, context)
