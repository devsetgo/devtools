# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from loguru import logger
from starlette.responses import RedirectResponse
from starlette_wtf import csrf_protect

from endpoints.pypi_check import forms
from endpoints.pypi_check import pypi_calls  # import main, process_raw
from endpoints.pypi_check.crud import get_request_group_id
from endpoints.pypi_check.crud import store_in_data
from resources import templates

base: str = "pypi"


@csrf_protect
async def pypi_index(request):

    form = await forms.RequirementsForm.from_formdata(request)
    form_data = await request.form()
    if await form.validate_on_submit():
        logger.critical(form_data)
        logger.info(form_data["requirements"])
        requirements_str = form_data["requirements"]
        raw_data: str = requirements_str
        # create UUID for request
        request_group_id = uuid.uuid4()
        # store incoming data
        # process raw data
        req_list = await pypi_calls.process_raw(raw_data=raw_data)
        # clean data
        cleaned_data = pypi_calls.clean_item(req_list)
        # call pypi
        fulllist = await pypi_calls.loop_calls_adv(
            itemList=cleaned_data, request_group_id=str(request_group_id)
        )
        # store returned results (bulk)

        values = {
            "id": str(uuid.uuid4()),
            "request_group_id": str(request_group_id),
            "text_in": raw_data,
            "json_data_in": req_list,
            "json_data_out": fulllist,
            "host_ip": request.client.host,
            "header_data": dict(request.headers),
            "dated_created": datetime.now(),
        }
        await store_in_data(values)
        # request_group_id = await main(raw_data=text_in, host_ip=host_ip)

        logger.info("Redirecting user to index page /")

        return RedirectResponse(
            url=f"/pypi/results/{str(request_group_id)}", status_code=303
        )
    status_code = 200
    template = f"/{base}/pypi_new.html"
    context = {"request": request, "form": form}
    logger.info("page accessed: /pypi/")
    return templates.TemplateResponse(template, context, status_code=status_code)


async def pypi_result(request):

    request_group_id = request.path_params["page"]

    data = await get_request_group_id(request_group_id=request_group_id)

    template = f"/{base}/result.html"
    context = {"request": request, "data": data}
    logger.info(f"page accessed: /pypi/{request_group_id}")
    return templates.TemplateResponse(template, context)


# async def pypi_process_stream(scope, receive, send):

#     # request_group_id = request.path_params["page"]

#     assert scope['type'] == 'http'
#     # request = Request(scope, receive, send)
#     generator = slow_numbers(1, 10)
#     response = StreamingResponse(generator, media_type='text/html')
#     await response(scope, receive, send)

# async def slow_numbers(minimum, maximum):
#     # yield('{% extends "/pypi/processing.html" %}{% block stream %}')
#     for number in range(minimum, maximum + 1):
#         yield '<li>%d</li>' % number
#         await asyncio.sleep(0.5)
#     # yield('{% endblock %}')


# async def app(scope, receive, send):
#     assert scope['type'] == 'http'
#     generator = slow_numbers(1, 10)
#     response = StreamingResponse(generator, media_type='text/html')
#     await response(scope, receive, send)
