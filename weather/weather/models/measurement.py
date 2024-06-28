from datetime import datetime

import pendulum
from sqladmin import ModelView
from sqlmodel import SQLModel, Field


class Measurement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    temp: float
    sunset: datetime
    sunrise: datetime
    temp_min: float
    temp_max: float
    desc: str
    weather_id: str
    city: str
    country: str
    ts: datetime
    pressure: int
    humidity: int
    wind_speed: float
    wind_deg: int
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: dict) -> "Measurement":
        return cls(
            temp=data["main"]["temp"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            desc=data["weather"][0]["main"],
            weather_id=data['weather'][0]['id'],
            sunset=pendulum.from_timestamp(data["sys"]["sunset"]),
            sunrise=pendulum.from_timestamp(data["sys"]["sunrise"]),
            ts=pendulum.from_timestamp(data['dt']),
            city=data['name'],
            country=data['sys']['country'].lower(),
            pressure=data['main']['pressure'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            wind_deg=data['wind']['deg'],
            latitude=data['coord']['lat'],
            longitude=data['coord']['lon'],
        )


class MeasurementAdmin(ModelView, model=Measurement):
    column_list = [Measurement.ts, Measurement.city, Measurement.country, Measurement.sunset, Measurement.sunrise,
                   Measurement.temp, Measurement.humidity, Measurement.pressure]
