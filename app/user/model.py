from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str
    full_name: str
    email: EmailStr
    hashed_password: str
    suspended: bool = Field(default=False)


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
