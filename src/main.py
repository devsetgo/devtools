# -*- coding: utf-8 -*-
from typing import Any
from typing import Dict

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Mount
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette_wtf import CSRFProtectMiddleware

import resources
import settings
from com_lib import exceptions
from com_lib import logging_config
from endpoints.health import endpoints as health_pages
from endpoints.main import endpoints as main_pages
from endpoints.modeler import endpoints as modeler_pages
from endpoints.pypi_check import endpoints as pypi_pages

logging_config.config_log()
resources.init_app()

routes = [
    Route("/", endpoint=main_pages.homepage, methods=["GET"]),
    Route("/index", endpoint=main_pages.index, methods=["GET"]),
    Route("/about", endpoint=main_pages.about_page, methods=["GET"]),
    Route("/health", endpoint=health_pages.health_status, methods=["GET"]),
    Mount(
        "/modeler",
        routes=[
            Route("/bpmn/viewer", endpoint=modeler_pages.viewer_bpmn, methods=["GET"]),
            Route(
                "/bpmn/modeler",
                endpoint=modeler_pages.modeler_bpmn,
                methods=["GET", "POST"],
            ),
        ],
        name="modeler",
    ),
    Route("/pypi", endpoint=pypi_pages.pypi_index, methods=["GET", "POST"]),
    Route(
        "/pypi/results/{page}",
        endpoint=pypi_pages.pypi_result,
        methods=["GET", "POST"],
    ),
    # Mount("/pypi/process",pypi_pages.pypi_process_stream),
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
]


middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    Middleware(CSRFProtectMiddleware, csrf_secret=settings.CSRF_SECRET),
]

exception_handlers: Dict[Any, Any] = {
    403: exceptions.not_allowed,
    404: exceptions.not_found,
    500: exceptions.server_error,
}


app = Starlette(
    debug=settings.DEBUG,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    on_startup=[resources.startup],
    on_shutdown=[resources.shutdown],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info", debug=settings.DEBUG)
