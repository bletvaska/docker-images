from http import HTTPStatus
from time import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import loguru


class AccessLog(BaseHTTPMiddleware):
    """
    Creates access log entry based on request and response.

    Args:
        BaseHTTPMiddleware: startlette base middleware class
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # prepare log message
        logger = loguru.logger.opt(colors=True)
        status = HTTPStatus(response.status_code).name.replace("_", " ").title()
        logger.info(
            f"{request.client.host}:{request.client.port} "
            f"{request.method} {request.url.path} <light-green>{response.status_code} {status}</light-green>"
        )

        return response


class AddProcessTimeHeader(BaseHTTPMiddleware):
    """
    Adds processing time to response header

    Args:
        BaseHTTPMiddleware: startlette base middleware class
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time()
        response = await call_next(request)
        process_time = (time() - start_time) * 1000
        response.headers["X-Process-Time"] = str(process_time)
        return response
