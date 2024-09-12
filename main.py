from fastapi import FastAPI, HTTPException, status
from schemas import GenreURLChoices, BandBase, BandWithID, BandCreate

app = FastAPI()

BANDS = [
    {"id": 1, "name": "The kinks", "genre": "Rock"},
    {"id": 1, "name": "The kinksoss", "genre": "Rock", "album": [
        {"title": "Master of Reality", "release_date": "1979-07-21"},
        {"title": "Master of Reality", "release_date": "1979-07-21"}
    ]},
    {"id": 2, "name": "Aphex Twin", "genre": "Electronic"},
    {"id": 3, "name": "Black Sabbath", "genre": "Metal", "album": [
        {"title": "Master of Reality", "release_date": "1979-07-21"},
        {"title": "Master of Reality", "release_date": "1979-07-21"}
    ]},
    {"id": 4, "name": "Wu-Tang clan", "genre": "Hip-Hop"},
]


@app.get("/bands")
async def bands(genre: GenreURLChoices | None = None, has_albums: bool = False) -> list[BandWithID]:
    # Band(**b)로 초기값 세팅이 가능한 이유는 BaseModel를 상속받기 때문이다.
    # Pydantic이 자동으로 __init__() 메서드를 생성
    # 1.	Pydantic의 BaseModel:
    # Pydantic의 BaseModel을 상속받는 클래스는 자동으로 데이터 검증 및 초기화를 위한 __init__() 메서드를 제공합니다.
    # Pydantic 모델은 클래스 속성을 필드로 사용하며, 이 필드들은 모델 인스턴스를 생성할 때 초기화되고 인스턴스 변수로 변경됩니다.

    # Query Parameter 쓸 경우, 값이 없을경우엔 반드시 default 값을 명시해야 한다.

    # if genre:
    #     if has_albums:
    #         return [
    #             Band(**b) for b in BANDS if b["genre"].lower() == genre.value and len(b.get("album", [])) > 0
    #         ]
    #     else:
    #         return [
    #             Band(**b) for b in BANDS if b["genre"].lower() == genre.value
    #         ]

    band_list = [BandWithID(**b) for b in BANDS]  # Band instance list

    if genre:
        # b["genre"]는 dict의 키 접근 방식이고
        # b.genre는 instance에서 속성 접근 방식
        band_list = [b for b in band_list if b.genre.value.lower()
                     == genre.value]

    if has_albums:
        band_list = [b for b in band_list if len(b.album) > 0]

    return band_list


@app.get("/bands/{band_id}")
async def band(band_id: int) -> BandWithID:
    band = next((BandWithID(**band)
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


@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band
