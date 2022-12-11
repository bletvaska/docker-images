# Weather App

Simple Weather app for my Docker 101 course. The info is taken from openweathermap.org.

## Tags

* [`latest`](https://github.com/bletvaska/docker-images/blob/master/weather/Dockerfile)
  , [`2022.01`](https://github.com/bletvaska/docker-images/blob/master/weather/Dockerfile)

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

## Available URLs

| endpoint     | method | description              | content type       |
|--------------|--------|--------------------------|--------------------|
| `/settings`  | `GET`  | list of current settings | `application/json` |
| `/weather`   | `GET`  | current weather          | `application/json` |
| `/`          | `GET`  | homepage                 | `text/html`        |



## Stolen Stuff

* icons: https://erikflowers.github.io/weather-icons/
* template: https://bbbootstrap.com/snippets/bootstrap-weather-info-template-19939290
