from enum import Enum
from datetime import date
from pydantic import BaseModel, model_validator


class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    METAL = "metal"
    HIP_HOP = "hip-hop"


class GenreChoices(Enum):
    ROCK = "Rock"
    ELECTRONIC = "Electronic"
    METAL = "Metal"
    HIP_HOP = "Hip-Hop"


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    album: list[Album] = []


class BandCreate(BandBase):
    # genre가 소문자, 대문자 입력 되더라도 첫글자를 강제로 대문자로 바꿔서 저장하기 위해 field_validator 사용
    @model_validator(mode="before")  # 자동변환 전에 수행하라는 뜻
    def title_case_genre(cls, values):
        # string.title() 문자열의 각 단어의 첫문자를 대문자로 만든다.
        values["genre"] = values.get('genre').title()

        return values


class BandWithID(BandBase):
    id: int
