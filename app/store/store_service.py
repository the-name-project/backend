from typing import List
from sqlmodel import Session,select,create_engine
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Query, status
from app.store.model import Store_Info
from app.store.menu.model import Menu
import pandas as pd
app = FastAPI()

sqlite_file_name = "test_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

session = Session(bind  = engine)
# ?skip=0&limit=10
@app.get('/stores',status_code=status.HTTP_200_OK)
async def get_stores(skip: int = 0, limit: int = 10,wheres:List[str]=Query(None)):
    Statement = select(Store_Info).offset(skip).limit(limit)
    data_info = session.exec(Statement).all()
    if data_info == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    df = []
    for  data in data_info:
        df.append(data.__dict__)
    df = pd.DataFrame(df)
    for where in wheres:
        filtered= df[df['address'].str.contains(where)]
    default = []

    for i in range(0,len(filtered.index)):
        which  = filtered.iloc[i].id
        Statement = select(Store_Info).where(Store_Info.id == int(which))
        data_info = session.exec(Statement).first()
        default.append(data_info)
    
    return default


@app.get('/store/{storeID}',response_model=Store_Info)
async def get_store(storeID:int):
    Statement = select(Store_Info).where(
        Store_Info.id == storeID
    )
    default = session.exec(Statement).first()

    if default == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return default

@app.get('/store/{storeID}/menu')
async def get_menu(storeID:int):
    Statement = select(Menu).where(
        Menu.store_id == storeID
    )
    default = session.exec(Statement).all()
    if default == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return default