import fastapi
from fastapi import Depends
from starlette.requests import Request

from rambo.dependencies import get_settings, get_title
from rambo.models.rambo import Rambo
from rambo.models.settings import Settings

router = fastapi.APIRouter()


@router.get('/data{extension}')
def get_data(request: Request, extension: str, rambo: Rambo = Depends(get_title)):
    return rambo
