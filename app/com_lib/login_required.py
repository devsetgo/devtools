# -*- coding: utf-8 -*-
from typing import Callable

from loguru import logger
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.responses import Response


def require_login(endpoint: Callable) -> Callable:
    async def check_login(request: Request) -> Response:
        if "username" not in request.session:
            logger.error(
                f"user page access without being logged in from {request.client.host}"
            )
            return RedirectResponse(url="/", status_code=303)

        return await endpoint(request)

    return check_login
