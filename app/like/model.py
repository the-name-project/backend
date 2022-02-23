from sqlmodel import Field, SQLModel
from typing import Optional

# Store Like Model
class StoreLike(SQLModel, table=True):
    store_id: Optional[int] = Field(default=None, foreign_key='store.id', primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='user.id', primary_key=True)
