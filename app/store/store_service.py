from operator import index
from re import S
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
    first = 0
    end = skip
    filtered = pd.DataFrame()
    
    while limit>len(filtered.index):
        first = end
        end=first+100
        Statement = select(Store_Info).offset(first).limit(100)
        data_info = session.exec(Statement).all()
        
        if data_info == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if len(data_info) == 0:
            break
        df = []
        
        for  data in data_info:
            df.append(data.__dict__)
        df = pd.DataFrame(df)
        if wheres:
            for where in wheres:
                df= df[df['address'].str.contains(where)]
        else:
            pass
        if len(filtered.index) ==0:
            filtered = df
        else:
            filtered = pd.concat([filtered,df])
        if len(filtered.index) > limit:
            
            while len(filtered.index) != limit:
                end=  int(filtered.iloc[len(filtered.index)-1].id)
                filtered = filtered[:-1]
    default = []
    
    for i in range(0,len(filtered.index)):
        which  = filtered.iloc[i].id
        Statement = select(Store_Info).where(Store_Info.id == int(which))
        data_info = session.exec(Statement).first()
        default.append(data_info)
    default.append({
        "end" : {end},
        "amount": {len(filtered.index)}
    })
    
    return default

@router.get('/naver_score',status_code=status.HTTP_200_OK)
async def get_stores(
        *,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10,
        wheres:List[str]=Query(None)):
    first = 0
    end = skip
    filtered = pd.DataFrame()
    
    while limit>len(filtered.index):
        first = end
        end=first+100
        Statement = select(Store_Info).where(Store_Info.naver_score!="None").order_by(Store_Info.naver_score.desc()).offset(first).limit(100)
        data_info = session.exec(Statement).all()
        
        if data_info == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if len(data_info) == 0:
            break
        df = []
        
        for  data in data_info:
            df.append(data.__dict__)
        df = pd.DataFrame(df)
        if wheres:
            for where in wheres:
                df= df[df['address'].str.contains(where)]
        else:
            pass
        if len(filtered.index) ==0:
            filtered = df
        else:
            filtered = pd.concat([filtered,df])
        if len(filtered.index) > limit:
            
            while len(filtered.index) != limit:
                end=  int(filtered.iloc[len(filtered.index)-1].id)
                filtered = filtered[:-1]
    default = []
    filtered = filtered.sort_values(by='naver_score' ,ascending=False)
    for i in range(0,len(filtered.index)):
        which  = filtered.iloc[i].id
        Statement = select(Store_Info).where(Store_Info.id == int(which))
        data_info = session.exec(Statement).first()
        default.append(data_info)
    default.append({
        "end" : {end},
        "amount": {len(filtered.index)}
    })
    
    return default

@router.get('/daumn_score',status_code=status.HTTP_200_OK)
async def get_stores(
        *,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10,
        wheres:List[str]=Query(None)):
    first = 0
    end = skip
    filtered = pd.DataFrame()
    
    while limit>len(filtered.index):
        first = end
        end=first+100
        Statement = select(Store_Info).where(Store_Info.daum_score!="None").order_by(Store_Info.daum_score.desc()).offset(first).limit(100)
        data_info = session.exec(Statement).all()
        
        if data_info == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if len(data_info) == 0:
            break
        df = []
        
        for  data in data_info:
            df.append(data.__dict__)
        df = pd.DataFrame(df)
        if wheres:
            for where in wheres:
                df= df[df['address'].str.contains(where)]
        else:
            pass
        if len(filtered.index) ==0:
            filtered = df
        else:
            filtered = pd.concat([filtered,df])
        if len(filtered.index) > limit:
            
            while len(filtered.index) != limit:
                end=  int(filtered.iloc[len(filtered.index)-1].id)
                filtered = filtered[:-1]
    default = []
    filtered = filtered.sort_values(by='daum_score' ,ascending=False)
    for i in range(0,len(filtered.index)):
        which  = filtered.iloc[i].id
        Statement = select(Store_Info).where(Store_Info.id == int(which))
        data_info = session.exec(Statement).first()
        default.append(data_info)
    default.append({
        "end" : {end},
        "amount": {len(filtered.index)}
    })
    
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