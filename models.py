from enum import Enum
from datetime import date
from pydantic import BaseModel, model_validator

from sqlmodel import SQLModel, Field, Relationship


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


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int = Field(default=None, foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # Relationship 정의
    # back_populates="album" 은 Band class의 album 변수를 가리킨다.
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None

    # genre가 소문자, 대문자 입력 되더라도 첫글자를 강제로 대문자로 바꿔서 저장하기 위해 field_validator 사용
    @model_validator(mode="before")  # 자동변환 전에 수행하라는 뜻
    def title_case_genre(cls, values):
        # string.title() 문자열의 각 단어의 첫문자를 대문자로 만든다.
        values["genre"] = values.get('genre').title()

        return values


class Band(BandBase, table=True):

    id: int = Field(default=None, primary_key=True)
    # Relationship 정의
    # back_populates ="band" band는 Album class의 band 변수를 가리킨다.
    albums: list[Album] = Relationship(back_populates="band")
