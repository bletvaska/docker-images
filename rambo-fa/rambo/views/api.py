import fastapi
from fastapi import Depends
from starlette.requests import Request

from rambo.dependencies import get_title

router = fastapi.APIRouter()


@router.get('/api/data{extension}')
def get_data(request: Request, extension: str, movie: dict = Depends(get_title)):
    return movie
