# Weather App

Simple Weather app for my Docker 101 course. The info is taken from openweathermap.org.


## Tags

* [`latest`](https://github.com/bletvaska/docker-images/blob/master/weather/Dockerfile)
  , [`2023.1`](https://github.com/bletvaska/docker-images/blob/master/weather/Dockerfile)
* [`2022.1`](https://github.com/bletvaska/docker-images/blob/master/weather/Dockerfile)


## Running the App

```bash
$ python -m weather.app
```

## Running the App in Container

```bash
$ docker container run --port 8000:8000 bletvaska/weather
```

## Environment Variables

Application can be controlled with following environment variables:

* `WEATHER_ENVIRONMENT` - Setting the environment, in which app will run. Possible values are `DEVELOPMENT`
  and `PRODUCTION`. When in dev environment, the debug logs will be seen also. Default is set to `PRODUCTION`.
* `WEATHER_UNITS` - Units specification for temperature. Possible values are `standard`, `metric` and `imperial`.
  Default is set to `metric`.
* `WEATHER_QUERY` - You can specify the name of the city you want the forecast for. Default is set to `kosice`.
* `WEATHER_UPDATE_INTERVAL` - Update interval in seconds. Min value is `15` and max value is `3600`. Default value is
  set to `60`.
* `WEATHER_DT_FORMAT` - Format of time and date. Currently set to ISO 8601 format (`"%Y-%m-%dT%H:%M:%SZ"`).
* `WEATHER_DB_URI` - Connection string for database according to
  [SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) documentation
* `WEATHER_THEME` - Theme selection. Possible values are `bitday` (default)


## Available URLs

| endpoint    | method | description                   | content type       |
|-------------|--------|-------------------------------|--------------------|
| `/`         | `GET`  | homepage                      | `text/html`        |
| `/healthz`  | `GET`  | healthcheck                   | `application/json` |
| `/history`  | `GET`  | returns all records from db   | `application/json` |
| `/admin`    | `GET`  | SQL Admin web page            | `text/html`        |
| `/settings` | `GET`  | list of current settings      | `application/json` |
| `/weather`  | `GET`  | current weather               | `application/json` |


## Healthcheck

When healthy, HTTP status code `200` is returned. When unhealthy, then `503` is returned.

To make service unhealthy, simply create empty file with name `unhealthy` in workdir (`/app`').


## Stolen Stuff

* icons: https://erikflowers.github.io/weather-icons/
* background images: bitday project
