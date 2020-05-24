# -*- coding: utf-8 -*-

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
from endpoints.health import endpoints as health_pages
from endpoints.main import endpoints as main_pages
from endpoints.pypi_check import endpoints as pypi_pages
from resources import init_app


routes = [
    Route("/", main_pages.index, name="dashboard", methods=["GET", "POST"]),
    Route("/about", main_pages.about_page, methods=["GET"]),
    Route("/health", endpoint=health_pages.health_status, methods=["GET"]),
    Route("/pypi", pypi_pages.pypi_index, name="PYPI", methods=["GET", "POST"]),
    Route(
        "/pypi/results/{page}",
        pypi_pages.pypi_result,
        name="PYPI Results",
        methods=["GET", "POST"],
    ),
    Mount("/static", app=StaticFiles(directory="statics"), name="static"),
]


middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
    Middleware(CSRFProtectMiddleware, csrf_secret=settings.CSRF_SECRET),
]

exception_handlers = {
    403: exceptions.not_allowed,
    404: exceptions.not_found,
    500: exceptions.server_error,
}


init_app()

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
