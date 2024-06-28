import uvicorn
from uvicorn.config import LOGGING_CONFIG

from rambo.dependencies import get_settings

settings = get_settings()
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"

uvicorn.run(
    'rambo.app:app',
    reload=settings.environment == 'dev',
    access_log=False,
    host='0.0.0.0'
)
