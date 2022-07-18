#!/usr/bin/env python3

import logging
import time
import os

import requests
from rich.logging import RichHandler

from .models import get_settings
from . import __version__


url_openweathermap = "http://api.openweathermap.org/data/2.5/weather?units={units}&q={query}&lang={language}&appid={token}"

# setup logging
logging.basicConfig(
    format="%(name)s  %(message)s",
    handlers=[RichHandler(
        show_path=False,
        omit_repeated_times=False,
        markup=True,
        )],
    datefmt="%Y-%m-%d %X"
)

logger = logging.getLogger("weather")


def main():
    # create settings
    settings = get_settings()

    # set logging
    if settings.environment == "development":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info(
        f"Weather Checker [bold cyan]{__version__}[/] is running in [bold green]{settings.environment.upper()}[/] environment."
    )
    logger.info(
        f'Weather conditions will be retrieved for "[bold yellow]{settings.query.capitalize()}[/]" every '
        f"[bold cyan]{settings.update_interval}[/] seconds.",
        extra={'highlighter': None}
    )
    logger.debug(settings)

    while True:
        try:
            # get weather data
            logger.debug("Requesting forecast...")
            url = url_openweathermap.format(**settings.dict())
            response = requests.get(url)

            # check status code
            if response.status_code != 200:
                raise requests.exceptions.RequestException('Wrong response.')

            # get data from service
            data = response.json()
            logger.debug("Received data:")
            logger.debug(data)

            # format dt
            dt_str = time.strftime(settings.dt_format, time.gmtime(data["dt"]))

            # log messages
            unit = "°C" if settings.units == "metric" else "K"
            logger.info(
                f'Last update for [bold yellow]{data["name"]} ({data["sys"]["country"]})[/] at: [bold purple]{dt_str}[/]',
                extra={'highlighter': None}
            )
            logger.info(f'It\'s [bold green]{data["weather"][0]["description"]}[/].')
            logger.info(
                f'temp=[bold cyan]{data["main"]["temp"]}[/]{unit} '
                f'pressure=[bold cyan]{data["main"]["pressure"]}[/]hPa '
                f'humidity=[bold cyan]{data["main"]["humidity"]}[/]%',
                extra={'highlighter': None}
            )

        except requests.exceptions.RequestException as ex:
            data = response.json()
            logger.error(f'HTTP Status Code: {response.status_code}')
            logger.error(data["message"])

        except Exception as ex:
            logger.exception(ex)

        time.sleep(settings.update_interval)


if __name__ == "__main__":
    main()
