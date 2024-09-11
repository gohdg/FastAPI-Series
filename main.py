from fastapi import FastAPI, HTTPException, status
from schemas import GenreURLChoices, Band

app = FastAPI()

BANDS = [
    {"id": 1, "name": "The kinks", "genre": "Rock"},
    {"id": 2, "name": "Aphex Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal", "album": [
        {"title": "Master of Reality", "release_date": "1979-07-21"},
        {"title": "Master of Reality", "release_date": "1979-07-21"}
    ]},
    {"id": 4, "name": "Wu-Tang clan", "genre": "Hip-Hop"},
]


@app.get("/bands")
async def bands() -> list[Band]:
    # Band(**b)로 초기값 세팅이 가능한 이유는 BaseModel를 상속받기 때문이다.
    # Pydantic이 자동으로 __init__() 메서드를 생성
    # 1.	Pydantic의 BaseModel:
    # Pydantic의 BaseModel을 상속받는 클래스는 자동으로 데이터 검증 및 초기화를 위한 __init__() 메서드를 제공합니다.
    # Pydantic 모델은 클래스 속성을 필드로 사용하며, 이 필드들은 모델 인스턴스를 생성할 때 초기화되고 인스턴스 변수로 변경됩니다.
    return [
        Band(**b) for b in BANDS
    ]


@app.get("/bands/{band_id}")
async def band(band_id: int) -> Band:
    band = next((Band(**band)
                for band in BANDS if band['id'] == band_id), None)

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
