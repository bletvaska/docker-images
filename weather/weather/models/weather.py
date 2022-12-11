from datetime import datetime

from pydantic import BaseModel


class Weather(BaseModel):
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

    @classmethod
    def from_dict(cls, data: dict) -> "Weather":
        return cls(
            temp=data["main"]["temp"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            desc=data["weather"][0]["main"],
            weather_id=data['weather'][0]['id'],
            sunset=data["sys"]["sunset"],
            sunrise=data["sys"]["sunrise"],
            ts=data['dt'],
            city=data['name'],
            country=data['sys']['country'].lower(),
            pressure=data['main']['pressure'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            wind_deg=data['wind']['deg'],
        )
