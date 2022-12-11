from datetime import datetime
import socket

import fastapi
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates

from rambo.dependencies import get_settings, get_jinja, get_title
from rambo.models.settings import Settings

router = fastapi.APIRouter()


@router.get('/')
def hello(request: Request, settings: Settings = Depends(get_settings),
          templates: Jinja2Templates = Depends(get_jinja)):
    data = {
        'request': request,
        'title': 'Rambo',
        'rambo': get_title(),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'current_date': datetime.utcnow().astimezone().replace(microsecond=0).isoformat(),
        'refresh_rate': settings.refresh_rate,
        'base_url': settings.base_url,
        'part': 1
    }

    return templates.TemplateResponse('home.html', data)
