from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import pendulum
from sqlmodel import Session, select

from .dependencies import get_settings, get_templates, get_session
from .models.settings import Settings
from .models.measurement import Measurement
from . import __version__

router = APIRouter()


def _translate(value, left_min, left_max, right_min, right_max):
    # print(value, left_min, left_max, right_min, right_max)
    return (value - left_min) * (right_max - right_min) / (left_max - left_min) + right_min


@router.get('/api/settings')
def get_settings(settings: Settings = Depends(get_settings)):
    return settings


@router.get('/api/weather')
def get_weather(session: Session = Depends(get_session)):
    # select last record from db
    statement = select(Measurement).order_by(Measurement.id.desc())
    weather = session.exec(statement).first()

    # return as dictionary
    return weather


@router.get('/api/history')
def get_history(session: Session = Depends(get_session), format: str = 'json'):
    # select all records from db
    statement = select(Measurement)
    data = session.exec(statement).all()

    # prepare output format

    return data


@router.get("/")
def homepage(request: Request, settings: Settings = Depends(get_settings),
             templates: Jinja2Templates = Depends(get_templates), session: Session = Depends(get_session)):

    # prepare context
    context = {
        "request": request,
        "base_url": settings.base_url,
        "refresh": settings.update_interval,
        "version": __version__,
        "environment": settings.environment,
    }

    # is valid token?
    if settings.token is None:
        context.update(
            message='Invalid or no API key!',
            title='Error'
        )
        return templates.TemplateResponse("plain.html", context)

    # select last record from db
    statement = select(Measurement).order_by(Measurement.id.desc())
    weather = session.exec(statement).first()

    now = pendulum.now(settings.timezone)
    sunrise = pendulum.instance(weather.sunrise).subtract(minutes=15)
    sunset = pendulum.instance(weather.sunset).add(minutes=15)

    # from IPython import embed; embed()
    # get background nr based on sunset, sunrise and now
    # is it a day now?
    if sunrise <= now <= sunset:
        value = _translate(now.timestamp(), sunrise.timestamp(), sunset.timestamp(), 1, 9)
        background_nr = int(value)
        print(f'night {background_nr}')
    else:
        # or is it night now?
        if sunset > now:
            value = _translate(now.timestamp(), sunset.subtract(days=1).timestamp(), sunrise.timestamp(), 10, 12)
        elif sunrise < now:
            value = _translate(now.timestamp(), sunset.timestamp(), sunrise.add(days=1).timestamp(), 10, 12)
        background_nr = int(value)
        print(f'day {background_nr}')

    context.update(
        now=now,
        background_nr=background_nr,
        weather=weather.dict(),
        title='Current Weather'
    )

    return templates.TemplateResponse("current.weather.html", context)
