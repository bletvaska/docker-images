import json
from functools import lru_cache
from pathlib import Path
from logging import getLogger

from starlette.templating import Jinja2Templates

from rambo.j2_filters import j2_duration
from rambo.models.settings import Settings

cwd = Path(__file__).parent
logger = getLogger('uvicorn.error')


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    logger.info(f"Loading settings for {settings.environment} environment.")
    return settings


@lru_cache
def get_jinja() -> Jinja2Templates:
    templates = Jinja2Templates(directory=cwd / 'templates/')

    # add filters
    templates.env.filters['duration'] = j2_duration

    return templates


@lru_cache
def get_title() -> dict:
    settings = get_settings()
    with open(cwd / 'db.json') as file:
        data = json.load(file)
        return data[settings.part - 1]
