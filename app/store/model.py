from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

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