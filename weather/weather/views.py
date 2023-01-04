from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import pendulum
from sqlmodel import Session, select

from .dependencies import get_settings, get_templates, get_session
from .models.settings import Settings
from .models.measurement import Measurement

router = APIRouter()

def _translate(value, left_min, left_max, right_min, right_max):
    # stolen from: https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another

    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


@router.get('/settings')
def get_settings(settings: Settings = Depends(get_settings)):
    return settings


@router.get('/weather')
def get_weather(session: Session = Depends(get_session)):
    # select last record from db
    statement = select(Measurement).order_by(Measurement.id.desc())
    weather = session.exec(statement).first()

    # return as dictionary
    return weather


@router.get('/history')
def get_history(session: Session = Depends(get_session), format: str = 'json'):
    # select all records from db
    statement = select(Measurement)
    data = session.exec(statement).all()

    # prepare output format

    return data


@router.get("/")
def homepage(request: Request, settings: Settings = Depends(get_settings),
                   templates: Jinja2Templates = Depends(get_templates), session: Session = Depends(get_session)):
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
    else:
        # or is it night now?
        if sunset > now:
            value = _translate(now.timestamp(), sunset.subtract(days=1).timestamp(), sunrise.timestamp(), 10, 12)
        elif sunrise < now:
            value = _translate(now.timestamp(), sunset.timestamp(), sunrise.add(days=1).timestamp(), 10, 12)
        background_nr = int(value)

    context = {
        "request": request,
        "refresh": settings.update_interval,
        "now": now,
        "background_nr": background_nr,
        "weather": weather.dict(),
        "version": "2022.12",
        "environment": settings.environment,
    }

    return templates.TemplateResponse("homepage.html", context)
