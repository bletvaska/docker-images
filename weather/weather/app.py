from contextlib import asynccontextmanager
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqladmin import Admin
from sqlmodel import create_engine, SQLModel
from starlette.staticfiles import StaticFiles

from .cron import retrieve_weather_data
from .middleware import AccessLog, AddProcessTimeHeader
from .dependencies import get_settings, get_logger
from .models.measurement import MeasurementAdmin
from . import __version__, views
from .api.service import router as service_router
from .api.healthcheck import router as healthcheck_router
# from .cron import router as cron_router, retrieve_weather_data


@asynccontextmanager
async def on_start(app: FastAPI):
    logger.debug(settings)

    logger.info(f"Weather Checker <cyan>{__version__}</cyan> is running in "
                f"<green>{settings.environment.upper()}</green> environment.")

    logger.info(f'Weather conditions will be retrieved for "<yellow>{settings.query.capitalize()}</yellow>" every '
                f"<cyan>{settings.update_interval}</cyan> seconds.")

    logger.info(f'Current Timezone is set to <green>{settings.timezone}</green>.')

    # uvicorn.run('weather.app:app', host='0.0.0.0', reload=True, log_level='error')

    # start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(retrieve_weather_data, "interval", minutes=1)
    scheduler.start()

    yield

    # teardown
    scheduler.shutdown()


# create settings object
settings = get_settings()

# enable additional colors in logger
logger = get_logger()

# setup app
app = FastAPI(lifespan=on_start)  # root_path=settings.path_prefix)
app.add_middleware(AccessLog)
app.add_middleware(AddProcessTimeHeader)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# services
app.include_router(service_router)
app.include_router(healthcheck_router)
app.include_router(views.router)

# init db
engine = create_engine(get_settings().db_uri)
SQLModel.metadata.create_all(engine)

# admin ui
admin = Admin(app, engine)
admin.add_view(MeasurementAdmin)
