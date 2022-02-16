from fastapi import FastAPI
from sqlalchemy.orm import query
from sqlmodel import select
from fastapi.encoders import jsonable_encoder

app = FastAPI()

dummy_data = [
    {
        "id": 1,
        "store": {
            "id": 1,
            "name": "Store1",
            "address": "Address1",
            "image": "https://pcmap.place.naver.com/restaurant/1215333269/home?entry=pll&from=nx&fromNxList=true&from=map&fromPanelNum=2&ts=1644984402140#"
        },
        "user": {
            "id": 1,
            "nickname": "user1",
            "full_name": "username1",
            "email": "user1@email.com",
            "hashed_password": 0,
        },
    },
    {
        "id": 2,
        "store": {
            "id": 2,
            "name": "Store2",
            "address": "Address2",
            "image": "https://pcmap.place.naver.com/restaurant/384834629/home?entry=pll&from=map&fromPanelNum=2&ts=1644984627192#"
        },
        "user": {
            "id": 1,
            "nickname": "user1",
            "full_name": "username1",
            "email": "user1@email.com",
            "hashed_password": 0,
        }
    },
    {
        "id": 3,
        "store": {
            "id": 2,
            "name": "Store2",
            "address": "Address2",
            "image": "https://pcmap.place.naver.com/restaurant/11604340/home?entry=pll&from=map&fromPanelNum=2&ts=1644987291170#"
        },
        "user": {
            "id": 2,
            "nickname": "user2",
            "full_name": "username2",
            "email": "user2@email.com",
            "hashed_password": 0,
        }
    }
]


# favorite
@app.get('/user/favorite')
async def read_favorite():
    # favorite = dummy_data.query.filter(dummy_data.user.id == user_id)
    return jsonable_encoder({"favorite": dummy_data})


# user favorite
@app.get('/user/{user_id}/favorite')
async def read_favorite(user_id: int):
    # favorite = dummy_data.query.filter(dummy_data.user.id == user_id)
    result = []
    for data in dummy_data:
        if data["user"]["id"] == user_id:
            result.append(data)

    return jsonable_encoder({"favorite": result})


if __name__ == "__main__":
    from os import system

    system("uvicorn app.main:app --reload")
