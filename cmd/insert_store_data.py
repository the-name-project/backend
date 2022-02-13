from sqlmodel import Session, create_engine
from app.store.model import Store_Info
from app.store.menu.model import Menu
import json

sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)#, echo=True

def read_json_and_make_data(filename):
    with open(filename, 'r') as jsonfile:
        json_datas = json.load(jsonfile)

    with Session(engine) as session:
        for store_name in json_datas:
            store_info = Store_Info(name = json_datas[store_name]['placeName']
                                    , address = json_datas[store_name]['placeAddress']
                                    , open_time = json_datas[store_name]['placeHour']
                                    , image = json_datas[store_name]['placeImgURL']
                                    , tags = json_datas[store_name]['placeTag']
                                    , tel_number = json_datas[store_name]['placeTel']
                                    , daum_score = json_datas[store_name]['placeKakaoReviewPoint']
                                    , naver_score = json_datas[store_name]['placeNaverReviewPoint'])
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
    from os import listdir
    result_file_dir = "../crawling_result/"
    for filename in listdir(result_file_dir):
        print(f"start {filename}")
        read_json_and_make_data(result_file_dir + filename)
        print(f"end {filename}")