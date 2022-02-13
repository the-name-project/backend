from app.poll.model import *
from app.store.model import Store_Info
from app.store.menu.model import Menu
from app.user.model import User
from app.user.favorite.model import *

from sqlmodel import SQLModel, create_engine

sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()