from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from ..store.model import Store_Info
from ..user.model import User


# 투표 모델
class Poll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    contents: List["PollContent"] = Relationship(back_populates="poll")
    vote: Optional["Vote"] = Relationship(back_populates="poll")
    user_list: List["User"] = Field(foreign_key="user.id")


# 투표
class Vote(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    poll_id: Optional[int] = Field(foreign_key="poll.id", default=None)
    poll: Optional["Poll"] = Relationship(back_populates="vote")

    content_id: Optional[str] = Field(foreign_key="poll_content.id", default=None)
    content: Optional["Poll_Content"] = Relationship(back_populates="vote")

    user_id: Optional["User"] = Field(foreign_key="user.id")


# 투표 내용
class Poll_Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(max_length=100, nullable=False)

    store_id: Optional[int] = Field(default=None, foreign_key="store_info.id")
    # store: Optional["Store"] = Relationship(back_populates="")

    poll_id: Optional[int] = Field(foreign_key="poll.id", default=None)
    poll: Optional["Poll"] = Relationship(back_populates="contents")

    vote_id: Optional[int] = Field(foreign_key="vote.id", default=None)
    # vote: List["Vote"] = Relationship(back_populates="")



from sqlmodel import SQLModel, create_engine

sqlite_file_name = "./test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()