from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from weather.dependencies import get_settings, get_templates, get_session
from weather.models.settings import Settings
from weather.models.weather import Weather

router = APIRouter()


@router.get('/settings')
def get_settings(settings: Settings = Depends(get_settings)):
    return settings


@router.get('/weather')
def get_weather(session: Session = Depends(get_session)):
    # select last record from db
    statement = select(Weather).order_by(Weather.id.desc())
    weather = session.exec(statement).first()

    # return as dictionary
    return weather


@router.get("/")
async def homepage(request: Request, settings: Settings = Depends(get_settings),
                   templates: Jinja2Templates = Depends(get_templates), session: Session = Depends(get_session)):
    # select last record from db
    statement = select(Weather).order_by(Weather.id.desc())
    weather = session.exec(statement).first()

    context = {"request": request}
    context.update(weather.dict())
    context['refresh'] = settings.update_interval

    return templates.TemplateResponse("homepage.html", context)
