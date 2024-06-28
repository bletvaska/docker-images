import sys
from functools import lru_cache
from pathlib import Path

from fastapi.templating import Jinja2Templates
from sqlmodel import create_engine, Session

from weather.models.settings import Settings


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    # logger.info(f"Loading settings for {settings.environment} environment.")
    return settings


@lru_cache
def get_templates() -> Jinja2Templates:
    return Jinja2Templates(directory=Path(__file__).parent / "templates")


def get_session() -> Session:
    engine = create_engine(get_settings().db_uri)
    with Session(engine) as session:
        yield session


@lru_cache
def get_logger():
    from loguru import logger
    logger = logger.opt(colors=True)  # ansi?
    logger.remove()
    logger.add(sys.stdout,
               format="<light-green>{time:YYYY-MM-DD HH:mm:ss}</light-green> <lw><level>{level:8}</level></lw> <level>{message}</level>",
               level=get_settings().log_level)

    return logger
