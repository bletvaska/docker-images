from contextlib import asynccontextmanager
from pathlib import Path
from logging import getLogger

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from .dependencies import get_title
from .helpers import get_quote
from .middleware import AddProcessTimeHeader
from .views.homepage import router as homepage_router
from .views.api import router as api_router

# init logger
logger = getLogger('uvicorn.error')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # print basic info
    movie = get_title()
    logger.info(f'{movie['title']} ({movie['year']})')
    logger.info(movie['plot'])

    # start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_quote, "interval", minutes=1)
    scheduler.start()

    logger.info('>> RAMBO is ready for action!')

    yield

    # teardown
    logger.info('>> RAMBO is going home. Bye!')
    scheduler.shutdown()


# init fastapi
app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')
app.include_router(homepage_router)
app.include_router(api_router)

# middleware config
app.add_middleware(AddProcessTimeHeader)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.info(f'{request.method} {request.url.path} {exc.status_code} {exc.detail}')

    return JSONResponse(
        {
            "message": exc.detail,
            "status_code": exc.status_code,
            "url": str(request.url),
        },
        status_code=exc.status_code
    )


def print_quote():
    quote = get_quote()
    logger.info(f'>> "{quote['quote']}" -- {quote['author']}')
