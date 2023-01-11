import sys
import time
from pathlib import Path
from fastapi_health import health

import requests
from loguru import logger
from fastapi import Depends, FastAPI, Request
from fastapi_utils.tasks import repeat_every
from sqladmin import Admin
import uvicorn
from sqlmodel import create_engine, SQLModel
from starlette.staticfiles import StaticFiles

from .middleware import AccessLog, AddProcessTimeHeader
from .dependencies import get_settings, get_session
from .models.measurement import Measurement, MeasurementAdmin
from . import __version__, views

# create settings object
settings = get_settings()

# enable additional colors in logger
logger = logger.opt(colors=True)  # ansi?
logger.remove()
logger.add(sys.stdout,
           format="<light-green>{time:YYYY-MM-DD HH:mm:ss}</light-green> <lw><level>{level:8}</level></lw> <level>{message}</level>",
           level=settings.log_level)

# setup app
app = FastAPI()
app.add_middleware(AccessLog)
app.add_middleware(AddProcessTimeHeader)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.include_router(views.router)

# init db
engine = create_engine(get_settings().db_uri)
SQLModel.metadata.create_all(engine)

# admin ui
admin = Admin(app, engine)
admin.add_view(MeasurementAdmin)

# healthcheck
def is_database_online(session: bool = Depends(get_session)):
    return session

def is_healthy():
    return not Path('unhealthy').exists()

app.add_api_route("/healthz", health([is_database_online, is_healthy]))


@app.on_event("startup")
@repeat_every(seconds=settings.update_interval)
def retrieve_weather_data() -> None:
    if settings.token is None:
        logger.error('No API key is provided. Check app settings.')
        return

    payload = {
        'units': settings.units,
        'q': settings.query,
        'lang': settings.language,
        'appid': settings.token
    }

    try:
        # get weather data
        logger.debug("Requesting forecast...")
        # url = url_openweathermap.format(**settings.dict())
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=payload)

        # check status code
        if response.status_code != 200:
            raise requests.exceptions.RequestException('Wrong response.')

        # get data from service
        data = response.json()
        logger.debug("Retrieved data:")
        logger.debug(data)

        weather = Measurement.from_dict(data)

        # format dt
        dt_str = time.strftime(settings.dt_format, time.gmtime(data["dt"]))

        # log messages
        unit = "°C" if settings.units == "metric" else "K"
        logger.info(
            f'Last update for <light-yellow>{weather.city} ({weather.country})</light-yellow> at: <light-magenta>{dt_str}</light-magenta>'
        )
        logger.info(f'Current condition is: <light-green>{weather.desc}</light-green>.')
        logger.info(
            f'temp: <light-cyan>{weather.temp}</light-cyan>{unit} '
            f'pressure: <light-cyan>{weather.pressure}</light-cyan>hPa '
            f'humidity: <light-cyan>{weather.humidity}</light-cyan>%'
        )

        # insert to db
        session = next(get_session())
        session.add(weather)
        session.commit()

    except requests.exceptions.RequestException as ex:
        data = response.json()
        logger.error(f'HTTP Status Code: {response.status_code}')
        logger.error(data["message"])

    except Exception as ex:
        logger.exception(ex)


def main():
    logger.debug(settings)

    logger.info(f"Weather Checker <cyan>{__version__}</cyan> is running in "
                f"<green>{settings.environment.upper()}</green> environment.")

    logger.info(f'Weather conditions will be retrieved for "<yellow>{settings.query.capitalize()}</yellow>" every '
                f"<cyan>{settings.update_interval}</cyan> seconds.")

    logger.info(f'Current Timezone is set to <green>{settings.timezone}</green>.')

    uvicorn.run('weather.app:app', host='0.0.0.0', reload=True, log_level='error')


if __name__ == '__main__':
    main()
