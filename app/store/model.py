from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


# Store Like Model
class StoreLike(SQLModel, table=True):
    store_id: int = Field(foreign_key='store_info.id', primary_key=True)
    user_id: int = Field(foreign_key='user.id', primary_key=True)


# Store Information
class Store_Info(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str

    open_time: Optional[str] = Field(default=None, nullable=True)
    image: Optional[str] = Field(default=None, nullable=True)
    tags: Optional[str] = Field(default=None, nullable=True)
    tel_number: Optional[str] = Field(default=None, nullable=True)

    naver_score: Optional[str] = Field(default=None, nullable=True)
    daum_score: Optional[str] = Field(default=None, nullable=True)

    menu: List['Menu'] = Relationship(back_populates='store_info')
    liked_user: List['User'] = Relationship(back_populates='liked_store', link_model=StoreLike)

    # review
    reviews: List["Review"] = Relationship(back_populates='store_info')
