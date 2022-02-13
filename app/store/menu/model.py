from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Menu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: str
    menu_image: Optional[str] = Field(default=None, nullable=True)

    store_id: Optional[int] = Field(default=None, foreign_key='store_info.id')
    store_info: Optional['Store_Info'] = Relationship(back_populates='menu')