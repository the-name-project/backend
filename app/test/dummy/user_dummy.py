from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from typing import Optional

from app.user.model import UserRead, User

app = FastAPI()

# user dummy data
# dummy_data = User(
#     id=1,
#     nickname="User1",
#     full_name="username1",
#     email="user1@email.com",
#     hashed_password="user1",
#     suspended=False
# )
dummy_data = [
    {
        "id": 1,
        "nickname": "user1",
        "full_name": "username1",
        "email": "user1@email.com",
        "hashed_password": 0,
    },
    {
        "id": 2,
        "nickname": "user2",
        "full_name": "username2",
        "email": "user2@email.com",
        "hashed_password": 0,
    }
]


# User Dummy Data
@app.get('/user')
async def read_user():
    # dummy_data.dict()
    return jsonable_encoder({"user": dummy_data})


# Users Dummy Data
@app.get('/user/{user_id}')
async def read_user(user_id: int):
    # dummy_data.dict()
    result = {}
    for data in dummy_data:
        if data["id"] == user_id:
            result = jsonable_encoder({"user": data})
            break

    return result


if __name__ == "__main__":
    from os import system

    system("uvicorn app.main:app --reload")
