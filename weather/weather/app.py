import sys
import time
from pathlib import Path

import requests
from loguru import logger
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
import uvicorn
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from weather.dependencies import get_settings
from weather.models.weather import Weather
from . import __version__

# enable additional colors in logger
logger = logger.opt(colors=True)  # ansi?
logger.remove()
logger.add(sys.stdout,
           format="<light-green>{time:YYYY-MM-DD HH:mm:ss}</light-green> <lw>{level:8}</lw> {message}",
           level='DEBUG')

# setup app
app = FastAPI()
settings = get_settings()
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# some globals
# TODO override this
weather = None


@app.get('/settings')
def get_settings():
    return settings


@app.get('/weather')
def get_weather():
    global weather
    return weather.dict()


@app.get("/")
async def homepage(request: Request):
    global weather
    context = {"request": request}
    context.update(weather.dict())
    context['refresh'] = settings.update_interval

    return templates.TemplateResponse("homepage.html", context)


@app.on_event("startup")
@repeat_every(seconds=settings.update_interval)
def retrieve_weather_data(*args, **kwargs) -> None:
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
        logger.debug("Received data:")
        logger.debug(data)

        global weather
        weather = Weather.from_dict(data)

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

    except requests.exceptions.RequestException as ex:
        data = response.json()
        logger.error(f'HTTP Status Code: {response.status_code}')
        logger.error(data["message"])

    except Exception as ex:
        logger.exception(ex)


def main():
    # create settings
    # settings = get_settings()
    logger.debug(settings)

    logger.info(f"Weather Checker <cyan>{__version__}</cyan> is running in "
                f"<green>{settings.environment.upper()}</green> environment.")

    logger.info(f'Weather conditions will be retrieved for "<yellow>{settings.query.capitalize()}</yellow>" every '
                f"<cyan>{settings.update_interval}</cyan> seconds.")

    uvicorn.run('weather.app:app', host='0.0.0.0', reload=True)  # , log_level='critical')


if __name__ == '__main__':
    main()
