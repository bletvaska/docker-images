import json
from pathlib import Path
from random import choice

from rambo.dependencies import get_settings


def get_quote() -> str:
    with open(Path(__file__).parent / 'static/quotes.json') as file:
        quotes = json.load(file)

        # return filter(lambda quote: quote['part'] == Settings().part, quotes)
        filtered = [quote for quote in quotes if quote['part'] == get_settings().part]
        return choice(filtered)

