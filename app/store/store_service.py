from typing import List
from sqlmodel import Session,select,create_engine
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Query, status
from app.store.model import Store_Info
from app.store.menu.model import Menu
import pandas as pd
from app.DB_session import get_session


router = APIRouter()

# ?skip=0&limit=10
@router.get('',status_code=status.HTTP_200_OK)
async def get_stores(
        *,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10,
        wheres:List[str]=Query(None)):
    Statement = select(Store_Info).offset(skip).limit(limit)
    data_info = session.exec(Statement).all()
    print("***********************8")
    print(data_info)
    if data_info == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    df = []
    for  data in data_info:
        df.append(data.__dict__)
    df = pd.DataFrame(df)
    print(df.head())
    if wheres:
        for where in wheres:
            filtered= df[df['address'].str.contains(where)]
    else:
        filtered = df
    default = []

    for i in range(0,len(filtered.index)):
        which  = filtered.iloc[i].id
        Statement = select(Store_Info).where(Store_Info.id == int(which))
        data_info = session.exec(Statement).first()
        default.append(data_info)
    
    return default


@router.get('/{storeID}',response_model=Store_Info)
async def get_store(
        *,
        session: Session = Depends(get_session),
        storeID:int):
    Statement = select(Store_Info).where(
        Store_Info.id == storeID
    )
    default = session.exec(Statement).first()

    if default == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return default

@router.get('/{storeID}/menu')
async def get_menu(
        *,
        session: Session = Depends(get_session),
        storeID:int):
    Statement = select(Menu).where(
        Menu.store_id == storeID
    )
    default = session.exec(Statement).all()
    if default == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return default