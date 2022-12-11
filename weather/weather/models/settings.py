from functools import lru_cache

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    db_uri: str = "sqlite:///db.sqlite"
    token = "08f5d8fd385c443eeff6608c643e0bc5"
    environment = "production"
    units = "metric"
    query = "kosice,sk"
    update_interval = 60
    language = "en"
    dt_format = "%Y-%m-%dT%H:%M:%SZ"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "weather_"

    @validator("units")
    def validate_units(cls, value):
        if value not in ("standard", "metric", "imperial"):
            raise ValueError(
                "Invalid units. Must be one of standard, metric or imperial."
            )
        return value

    @validator("language")
    def validate_language(cls, value):
        languages = (
            "af",
            "al",
            "ar",
            "az",
            "bg",
            "ca",
            "cz",
            "da",
            "de",
            "el",
            "en",
            "eu",
            "fa",
            "fi",
            "fr",
            "gl",
            "he",
            "hi",
            "hr",
            "hu",
            "id",
            "it",
            "ja",
            "kr",
            "la",
            "lt",
            "mk",
            "no",
            "nl",
            "pl",
            "pt",
            "pt_br",
            "ro",
            "ru",
            "sv",
            "se",
            "sk",
            "sl",
            "sp",
            "es",
            "sr",
            "th",
            "tr",
            "ua",
            "uk",
            "vi",
            "zh_cn",
            "zh_tw",
            "zu",
        )
        if value not in languages:
            raise ValueError(
                f'Invalid language. Must be one of {", ".join(languages)}.'
            )
        return value

    @validator("update_interval")
    def validate_update_interval(cls, value):
        if value < 15 or value > 60 * 60:
            raise ValueError(
                "Invalid update interval. Interval must be integer number between 15 and 3600 seconds."
            )
        return value

    @validator("environment")
    def validate_environment(cls, value):
        if value.lower() in ("development", "dev", "devel"):
            return "development"

        if value.lower() in ("production", "prod"):
            return "production"

        raise ValueError("Invalid environment. Should be DEVELOPMENT or PRODUCTION.")
