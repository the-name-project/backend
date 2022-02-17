from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.responses import RedirectResponse

from sqlmodel import SQLModel, create_engine

sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(bind=engine)


@app.get("/", response_class=RedirectResponse)
def root() -> str:
    return "/docs"