from fastapi import FastAPI, HTTPException, status
from enum import Enum


app = FastAPI()


class GenreURLChoices(Enum):
    ROCK = "rock"
    ELECTRONIC = "electronic"
    METAL = "metal"
    HIP_HOP = "hip-hop"


BANDS = [
    {"id": 1, "name": "The kinks", "genre": "Rock"},
    {"id": 2, "name": "Aphex Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal"},
    {"id": 4, "name": "Wu-Tang clan", "genre": "Hip-Hop"},
]


@app.get("/bands")
async def bands() -> list[dict]:
    return BANDS


@app.get("/bands/{band_id}")
async def band(band_id: int) -> dict:
    band = next((band for band in BANDS if band['id'] == band_id), None)

    if band is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Band not found")

    return band


@app.get("/bands/genre/{genre}")
async def band_for_genre(genre: GenreURLChoices) -> list[dict]:
    # Fastapi는 사용자가 입력한 path paramter를 이용해서 GenreURLChoicse의 열거형 객체를 찾아서 반환한다.
    # 그후 genre는 사용자 입력값이 아닌, GenreURLChoices.ROCK, GenreURLChoices.ELECTRONIC 등과 같은 열거형 객체로 변환된다.
    # genre가 열거형객체이므로, 그 값에 접근하기위해 .value 속성을 사용해서 값에 접근한것이다. 아래코드
    band = [band for band in BANDS if band["genre"].lower() == genre.value]

    return band
