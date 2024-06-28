from typing import Literal

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    base_url: AnyHttpUrl = 'http://localhost:8000'
    refresh_rate: int = 1
    part: int = 1
    environment: Literal['dev', 'prod'] = 'prod'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'rambo_'
