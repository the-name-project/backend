from typing import Optional, List, TYPE_CHECKING, Any
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.user.model import User
    from app.store.model import Store_Info


# # Image
# class Image(SQLModel):

# Review Create
class ReviewCreate(SQLModel):
    content: str


# Review Read
class ReviewRead(SQLModel):
    id: int
    content: str
    store_id: Any
    user_id: Any


# Review Update
class ReviewUpdate(SQLModel):
    content: str


# Review
class Review(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str = Field(max_length=150, nullable=False)

    store_id: int = Field(foreign_key='store_info.id')
    store_info: "Store_Info" = Relationship(back_populates='reviews')

    user_id: int = Field(foreign_key='user.id')
    user: "User" = Relationship(back_populates='reviews')

