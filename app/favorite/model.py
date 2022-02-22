from sqlmodel import Field, SQLModel


class StoreFavorite(SQLModel,table =True):
    store_id: int = Field(foreign_key='store_info.id', primary_key=True)
    user_id: int = Field(foreign_key='user.id', primary_key=True)