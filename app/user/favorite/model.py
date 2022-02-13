from typing import Optional,List
from sqlmodel import Field, Relationship,  SQLModel

from app.store.model import Store_Info
from app.user.model import User


class poll_favorite(SQLModel, table  = True):
    id: Optional[int] = Field(default=None,primary_key=True)

    store_id : Optional[int] = Field(default=None,foreign_key="store_info.id")
    store : Optional["Store_Info"] = Relationship(back_populates="poll_favorite")

    user_id : Optional[int] = Field(default=None, foreign_key="User.id")
    user: Optional["User"] = Relationship(back_populates="poll_favorite")
