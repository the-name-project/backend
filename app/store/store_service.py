from sqlmodel import Field, Session,select,create_engine
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, status
from app.store.model import Store_Info
from app.store.menu.model import Menu
app = FastAPI()

sqlite_file_name = "test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

session = Session(bind  = engine)
# ?skip=0&limit=10
@app.get('/stores',status_code=status.HTTP_200_OK)
async def get_stores(skip: int = 0, limit: int = 10):
    Statement = select(Store_Info).offset(skip).limit(limit)
    deafult = session.exec(Statement).all()

    if deafult == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #default는 배열로 json형식의 값들을 보냄
    return deafult


@app.get('/store/{storeID}',response_model=Store_Info)
async def get_store(storeID:int):
    Statement = select(Store_Info).where(
        Store_Info.id == storeID
    )
    deafult = session.exec(Statement).first()

    if deafult == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return deafult

@app.get('/store/{storeID}/menu')
async def get_menu(storeID:int):
    Statement = select(Menu).where(
        Menu.store_id == storeID
    )
    deafult = session.exec(Statement).all()
    if deafult == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return deafult