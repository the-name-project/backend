from typing import Optional, List
from sqlmodel import Field, Session, SQLModel, create_engine, Relationship
import json

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


class Menu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: str
    menu_image: Optional[str] = Field(default=None, nullable=True)

    store_id: Optional[int] = Field(default=None, foreign_key='store_info.id')
    store_info: Optional['Store_Info'] = Relationship(back_populates='menu')


sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def read_json_and_make_data(filename = '중구.json'):
    with open(filename, 'r') as jsonfile:
        json_datas = json.load(jsonfile)

    with Session(engine) as session:
        for store_name in json_datas:
            print(store_name)
            store_info = Store_Info(name = json_datas[store_name]['placeName']
                                    , address = json_datas[store_name]['placeAddress']
                                    , open_time = json_datas[store_name]['placeHour']
                                    , image = json_datas[store_name]['placeImgURL']
                                    , tags = json_datas[store_name]['placeTag']
                                    , tel_number = json_datas[store_name]['placeTel']
                                    , daum_score = json_datas[store_name]['placeReviewPoint'])
            session.add(store_info)
            session.commit()
            for menu in json_datas[store_name]['placeMenu']:
                menu_info = Menu(name = json_datas[store_name]['placeMenu'][menu]['menuName']
                                 , price = json_datas[store_name]['placeMenu'][menu]['menuPrice']
                                 , menu_image = json_datas[store_name]['placeMenu'][menu]['menuImg']
                                 , store_id = store_info.id)
                session.add(menu_info)
            session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    read_json_and_make_data()