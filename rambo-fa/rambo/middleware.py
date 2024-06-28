from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from rambo.dependencies import get_title


class AddProcessTimeHeader(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        movie = get_title()
        response.headers['X-Title'] = movie['title']
        response.headers['X-Request-Url'] = str(request.url)

        return response
