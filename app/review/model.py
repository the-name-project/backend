from typing import Optional, List, TYPE_CHECKING, Any
from sqlmodel import Field, SQLModel, Relationship

# Review
class Review_info(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str = Field(max_length=150, nullable=False)

    store_id: int = Field(default=None, foreign_key='store.id')
    store: "Store" = Relationship(back_populates='reviews')
    user_id: int = Field(default=None, foreign_key='user.id')
    user: "User" = Relationship(back_populates='reviews')

# Review Create
class ReviewCreate(SQLModel):
    content: str


# Review Read
class ReviewRead(SQLModel):
    id: int
    content: str
    store: Any
    user: Any


# Review Update
class ReviewUpdate(SQLModel):
    content: str
