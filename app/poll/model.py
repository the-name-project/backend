from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.store.model import Store_Info
from app.user.model import User
from app.store.model import Store_Info


# 투표 모델
class Poll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    contents: List["PollContent"] = Relationship(back_populates="poll")
    vote: List["Vote"] = Relationship(back_populates="poll")
    user_list: List["User"] = Relationship(back_populates="poll")


# 투표 내용
class Poll_Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(max_length=100, nullable=False)

    store_id: Optional[int] = Field(default=None, foreign_key="store_info.id")
    store: Optional["Store_Info"] = Relationship(back_populates="poll_content")

    poll_id: Optional[int] = Field(foreign_key="poll.id", default=None)
    poll: Optional["Poll"] = Relationship(back_populates="contents")

    vote: List["Vote"] = Relationship(back_populates="poll_content")

# 투표
class Vote(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    poll_id: Optional[int] = Field(foreign_key="poll.id", default=None)
    poll: Optional["Poll"] = Relationship(back_populates="vote")

    content_id: Optional[str] = Field(foreign_key="poll_content.id", default=None)
    content: Optional["Poll_Content"] = Relationship(back_populates="vote")

    user_id: List["User"] = Relationship(back_populates='vote')


