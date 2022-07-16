#!/usr/bin/env python3

import logging
from time import sleep
import time

import requests

from .models import get_settings
from . import __version__

url_openweathermap = 'http://api.openweathermap.org/data/2.5/weather?units={units}&q={query}&lang={language}&appid={token}'

logger = logging.getLogger('weather')
logging.basicConfig(format='%(asctime)s  %(name)s  %(levelname)5s: %(message)s')


def main():
    # create settings
    settings = get_settings()

    # set logging
    if settings.environment == 'development':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info(f"Weather Checker {__version__} is running in {settings.environment.upper()} environment with update interval {settings.update_interval} secs.")
    logger.debug(settings)

    while True:
        # get weather data
        logger.debug('Requesting forecast...')
        url = url_openweathermap.format(**settings.dict())
        response = requests.get(url)

        # get data from service
        data = response.json()
        logger.debug('Received data:')
        logger.debug(data)

        # format dt
        dt_str = time.strftime(settings.dt_format, time.gmtime(data['dt']))

        # log messages
        unit = '°C' if settings.units == 'metric' else 'K'
        logger.info(f'Last update for {data["name"]} ({data["sys"]["country"]}) at: {dt_str}')
        logger.info(f'temp={data["main"]["temp"]}{unit} pressure={data["main"]["pressure"]}hPa humidity={data["main"]["humidity"]}%')

        sleep(settings.update_interval)


if __name__ == '__main__':
    main()
