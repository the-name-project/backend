from sqlmodel import Session, create_engine
from app.store.model import Store
from app.store.menu.model import Menu
import json

sqlite_file_name = "../test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)#, echo=True

def is_under_price(raw_price_info : str) -> (bool, int):
    raw_price_info = raw_price_info.replace(',', '', 3).strip()
    if '~' in raw_price_info:
        raw_price_info = raw_price_info[raw_price_info.find('~')+1:]
    start_index = 0
    detact_number = False
    int_price = 999999
    for index, char in enumerate(raw_price_info):
        if not char.isnumeric():    #not number
            if detact_number:
                int_price = int(raw_price_info[start_index:index])
            else:
                start_index = index
        else:
            if index == len(raw_price_info) - 1:
                int_price = int(raw_price_info[start_index:])
            else:
                detact_number = True
    if int_price <= 10000:
        under_price = True
    else:
        under_price = False
    return (under_price, int_price)

def read_json_and_make_data(filename):
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        json_datas = json.load(jsonfile)

    with Session(engine) as session:
        for store_name in json_datas:
            price_data = {True:0, False:0}
            for menu in json_datas[store_name]['placeMenu']:
                is_under, _ = is_under_price(json_datas[store_name]['placeMenu'][menu]['menuPrice'])
                price_data[is_under] += 1
            if price_data[True] > 3:
                store_info = Store(name = json_datas[store_name]['placeName']
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
                    _, int_price = is_under_price(json_datas[store_name]['placeMenu'][menu]['menuPrice'])
                    menu_info = Menu(name = json_datas[store_name]['placeMenu'][menu]['menuName']
                                     , price = str(int_price)
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