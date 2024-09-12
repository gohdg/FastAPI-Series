from fastapi import FastAPI, HTTPException, status, Path, Query, Depends
from models import Album, GenreURLChoices, Band, BandCreate
from sqlmodel import Session, select
from typing import Annotated
from contextlib import asynccontextmanager
from db import init_db, get_session

# FastAPI Lifespan Events
# application이 starts up 하기전에 한번 수행
# 또한 application이 shuting down될때 실행된다.
# from contextlib import asynccontextmanager
# @asynccontextmanager decorator와 함께 해당 event 함수를 정의


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:

    band_list = session.exec(select(Band)).all()

    if genre:
        # b["genre"]는 dict의 키 접근 방식이고
        # b.genre는 instance에서 속성 접근 방식
        band_list = [b for b in band_list if b.genre.value.lower()
                     == genre.value]

    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list


@app.get("/bands/{band_id}")
async def band(
    band_id: Annotated[int, Path(title="The band ID")],
    session: Session = Depends(get_session)
) -> Band:
    # Band data 가져오기
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Band not found")

    return band


# @app.get("/bands/genre/{genre}")
# async def band_for_genre(genre: GenreURLChoices) -> list[dict]:
#     # Fastapi는 사용자가 입력한 path paramter를 이용해서 GenreURLChoicse의 열거형 객체를 찾아서 반환한다.
#     # 그후 genre는 사용자 입력값이 아닌, GenreURLChoices.ROCK, GenreURLChoices.ELECTRONIC 등과 같은 열거형 객체로 변환된다.
#     # genre가 열거형객체이므로, 그 값에 접근하기위해 .value 속성을 사용해서 값에 접근한것이다. 아래코드
#     band = [band for band in BANDS if band["genre"].lower() == genre.value]

#     return band


@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title,
                release_date=album.release_date,
                band=band
            )
            session.add(album_obj)
    session.commit()
    # refresh하는 이유 commit 후에 id가 생성되는데 refresh 전까지 band object는 id가 없는 상태. band refresh 하면 id값이 band에 저장된다
    # session.refresh(band)를 호출하면 데이터베이스에서 band 객체를 다시 읽어와서 band에 최신 상태의 값을 채워주게 됩니다. 이 작업은 commit() 이후에 객체가 데이터베이스에 제대로 반영되었는지 확인하고, 자동 생성된 id나 기타 변경된 필드를 가져오기 위해 필요
    session.refresh(band)

    return band
