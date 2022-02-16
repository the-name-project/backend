from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

app = FastAPI()


dummy_data = [
    {
        "id": 1,
        "content": "테스트 리뷰1 입니다!",
        "created_at": "2022/02.16",
        "user": {
            "id": 1,
            "nickname": "user1",
            "full_name": "username1",
            "email": "user1@email.com",
            "hashed_password": 0,
        },
        "menu": {
            "id": 1,
            "name": "생긴것도 이상한 테스트 삼겹살",
            "price": 16000,
            "menu_image": "https://search.pstatic.net/sunny/?src=http%3A%2F%2Fimg2.tmon.kr%2Fcdn3%2Fdeals%2F2021%2F07%2F02%2F6733939954%2Ffront_30a41_abx4n.jpg&type=a340",
            "store": {
                "id": 1
            }
        }
    }
]


# User Review
@app.get('/user/{user_id}/review')
async def read_review(user_id: int):
    result = []
    for data in dummy_data:
        if data["user"]["id"] == user_id:
            result.append(data)

    return jsonable_encoder({"review": result})
