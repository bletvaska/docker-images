import socket
from logging import getLogger

import fastapi
import pendulum
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates

from rambo.dependencies import get_settings, get_jinja, get_title
from rambo.models.settings import Settings

router = fastapi.APIRouter()
logger = getLogger('uvicorn.error')


@router.get('/')
def hello(request: Request, settings: Settings = Depends(get_settings),
          jinja: Jinja2Templates = Depends(get_jinja)):
    logger.info('>> RAMBO received a request!')

    data = {
        'request': request,
        'movie': get_title(),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'current_date': pendulum.now().to_iso8601_string(),
        'refresh_rate': settings.refresh_rate,
        'base_url': settings.base_url,
        'part': settings.part
    }

    return jinja.TemplateResponse('index.html', data)
