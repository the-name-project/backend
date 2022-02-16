from sqlmodel import Session, create_engine
from typing import Generator

sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session
