from pydantic import BaseModel, HttpUrl, root_validator, validator, Field


class Rambo(BaseModel):
    title: str = Field(alias="Title")
    year: str = Field(alias='Year')
    description: str = Field(alias='Plot')
    part: int
    imdb_id: str = Field(alias='imdbID')
    url: HttpUrl = None
    poster: HttpUrl = Field(alias="Poster")
    rating: str = Field(alias='Ratings')

    @validator('url', pre=True, always=True )
    def get_imdb_url(cls, v, values):
        return f'https://www.imdb.com/title/{values["imdb_id"]}'

    @validator('rating', pre=True, always=True)
    def get_ratings(cls, v):
        return v[0]['Value']
