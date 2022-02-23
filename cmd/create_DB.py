from app.favorite.model import StoreFavorite
from app.like.model import StoreLike
from app.review.model import Review_info
from app.store.model import Store
from app.store.menu.model import Menu
from app.user.model import User


from sqlmodel import SQLModel, create_engine

sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()