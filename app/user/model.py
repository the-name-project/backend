from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr

from app.store.model import StoreLike,StoreFavorite

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str
    full_name: str
    email: EmailStr
    hashed_password: str
    suspended: bool = Field(default=False)

    # StoreLike <-> User 다대다
    liked_store: List['Store_Info'] = Relationship(back_populates='liked_user', link_model=StoreLike)
    favorite_store: List['Store_Info'] = Relationship(back_populates='favorite_user', link_model=StoreFavorite)

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
