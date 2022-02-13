from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from app.store.model import Store_Info
from app.user.model import User


# 다대다 투표, 유저 링크 모델
class PollUserLink(SQLModel):
    __tablename__ = "poll_user_link"
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    poll_id: Optional[int] = Field(default=None, foreign_key="poll.id", primary_key=True)


# 투표 모델
class Poll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    contents: List["PollContent"] = Relationship(back_populates="poll")

    # 다대다 -> Poll
    user_list: List["User"] = Relationship(back_populates="poll_list", link_model="PollUserLink")

    # 다대다 -> User 모델로..
    # poll_list: List["Poll"] = Relationship(back_populates="user_list", link_model="PollUserLink")


# 투표 내용
class PollContent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=100, nullable=False)

    # PollContent 1:1 Store_Info
    store_id: Optional[int] = Field(default=None, foreign_key="store_info.id")
    store: Optional["Store_Info"] = Relationship(back_populates="poll_content")

    # Poll 1:N PollContent
    poll_id: Optional[int] = Field(foreign_key="poll.id", default=None)
    poll: Optional["Poll"] = Relationship(back_populates="contents")

    # link_model -> 다대다 연결, "polls" -> User 모델 연결
    # polls: List["PollContent"] = Relationship(back_populates="polled_users", link_model="Vote") --> User 모델에 추가
    polled_users: List["User"] = Relationship(back_populates="polls", link_model="Vote")


# 투표
class Vote(SQLModel):
    __tablename__ = "poll_vote"
    # User 모델 연결
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)

    # PollContent 모델 연결
    poll_content_id: int = Field(default=None, foreign_key="poll_content.id", primary_key=True)


# Poll Read
class PollRead(SQLModel):
    id: int
    title: str
    contents: List[str]
    user_list: List[str]


from sqlmodel import SQLModel, create_engine

sqlite_file_name = "./test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
#
#
# if __name__ == "__main__":
#     create_db_and_tables()
