from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import sessionmaker

from sqlmodel import SQLModel, create_engine

# # SQLite3
# sqlite_file_name = "../test_database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
#
# engine = create_engine(sqlite_url, echo=True, encoding='utf-8')


# MySQL
# mysql 연동
app = {
    'name': 'mysql+pymysql',
    'user': 'root',
    'password': '1234',
    'host': '127.0.0.1',
    'dbconn': 'fast_test',
    'port': '3306'
}


SQLALCHEMY_DATABASE_URL = f'{app["name"]}://{app["user"]}:{app["password"]}@{app["host"]}:{app["port"]}/{app["dbconn"]}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True
)

SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(bind=engine)


@app.get("/", response_class=RedirectResponse)
def root() -> str:
    return "/docs"

# if __name__ == "__main__":
#     from os import system
#     system("uvicorn app.main:app --reload")