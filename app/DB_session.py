from sqlmodel import Session, create_engine
from typing import Generator
import secrets

sqlite_file_name = "test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

SECRET_KEY: str = secrets.token_urlsafe(32)

def get_session() -> Generator:
    with Session(engine) as session:
        return session
