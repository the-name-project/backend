from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from sqlalchemy.orm.relationships import RelationshipProperty
from app.like.model import StoreLike
from app.favorite.model import StoreFavorite
from app.review.model import Review_info

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str
    full_name: str
    email: EmailStr
    hashed_password: str
    suspended: bool = Field(default=False)

    # StoreLike <-> User 다대다
    liked_store: List['Store'] = Relationship(back_populates='liked_user', link_model=StoreLike)
    
    # storeFavorite
    favorite_store: List['Store'] = Relationship(back_populates='favorite_user', link_model=StoreFavorite)

    # review
    review_store: List["Store"] = Relationship(back_populates='review_user',link_model=Review_info)


class UserCreate(SQLModel):
    nickname: str
    full_name: str
    email: EmailStr
    hashed_password: str


class UserRead(SQLModel):
    id: int
    nickname: str
    full_name: str
    email: EmailStr
    hashed_password: str
    suspended: bool


class UserUpdate(SQLModel):
    nickname: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
