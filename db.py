from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///db.sqlite"

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    # DB initialization

    # metadata.create_all models.py에 있는 class 중 table=true 라고 정의한것을 기준으로 table 생성
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session  # session을 반환하고 일시중지
