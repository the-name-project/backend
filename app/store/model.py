from typing import Optional, List, Any
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from app.favorite.model import StoreFavorite
from app.user.model import User
from app.like.model import StoreLike
from app.review.model import Review_info

# Store Information
class Store(SQLModel, table=True):
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
    liked_user: List[User] = Relationship(back_populates='liked_store', link_model=StoreLike)
    favorite_user: List[User] = Relationship(back_populates='favorite_store', link_model=StoreFavorite)
    # review
    reviews: List['Review_info'] = Relationship(back_populates='store')


class StoreRead(SQLModel):
    id: int
    name: str
    address: str

    open_time: Optional[str]
    image: Optional[str]
    tags: Optional[str]
    tel_number: Optional[str]

    naver_score: Optional[str]
    daum_score: Optional[str]

    menu: Any
    liked_user: Any
    favorite_user: Any

    reviews: Any
