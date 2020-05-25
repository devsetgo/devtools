# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from loguru import logger

import settings


def config_log():
    """
    Logging configuration for loguru and standard logging
    Intercepting of standard logging to loguru included

    """
    logger.remove()
    log_path = Path.cwd().joinpath("log").joinpath("app_log.log")
    logger.add(
        log_path,
        level=settings.LOGURU_LOGGING_LEVEL,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        enqueue=True,
        backtrace=False,
        rotation=settings.LOGURU_ROTATION,
        retention=settings.LOGURU_RETENTION,
        compression="zip",
        serialize=False,
    )

    class InterceptHandler(logging.Handler):
        def emit(self, record):

            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())

    logging.basicConfig(
        handlers=[InterceptHandler()], level=settings.LOGURU_LOGGING_LEVEL
    )
