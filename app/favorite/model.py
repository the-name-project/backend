from sqlmodel import Field, SQLModel


class StoreFavorite(SQLModel,table =True):
    store_id: int = Field(default=None, foreign_key='store.id', primary_key=True)
    user_id: int = Field(default=None, foreign_key='user.id', primary_key=True)