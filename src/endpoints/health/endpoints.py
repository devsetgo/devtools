# -*- coding: utf-8 -*-
"""
Application health endpoints
"""
from loguru import logger
from starlette.responses import JSONResponse


async def health_status(request):
    """
    Application status endpoint with response of UP
    """
    logger.info(f"health accessed from ip address: {request.client.host}")
    return JSONResponse({"status": "UP"})
