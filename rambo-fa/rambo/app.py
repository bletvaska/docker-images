from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from .views import homepage, data

# init fastapi
app = FastAPI()
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')
app.include_router(homepage.router)
app.include_router(data.router)

