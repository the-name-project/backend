from typing import List
from sqlmodel import Session,select
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, Query, status
import pandas as pd

from app.DB_session import get_session
from app.store.model import Store_Info
from app.store.menu.model import Menu
from app.user.model import User
from app.user.service import get_current_user
from app.store.service import service

router = APIRouter()


@router.get('',status_code=status.HTTP_200_OK)
async def get_stores(
        *,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10,
        wheres:List[str]=Query(None)):
    return service.filter_store(session,skip=skip,limit=limit,wheres=wheres)
    

@router.get('/naver_score',status_code=status.HTTP_200_OK)
async def get_sorted_stores_by_naver(
        *,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10,
        wheres:List[str]=Query(None)):
    return service.filter_store_naver(session,skip=skip,limit=limit,wheres=wheres)

@router.get('/daum_score',status_code=status.HTTP_200_OK)
async def get_sorted_stores_by_kakao(
        *,
        session: Session = Depends(get_session),
        skip: int = 0,
        limit: int = 10,
        wheres:List[str]=Query(None)):
    return service.filter_store_kakao(session,skip=skip,limit=limit,wheres=wheres)

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


# 가게 좋아요 기능
@router.post('/{store_id}/likes', status_code=status.HTTP_204_NO_CONTENT)
def do_like_store(
        *,
        session: Session = Depends(get_session),
        store_id: int,
        current_user: User = Depends(get_current_user)
):
    service.like_store(session, store_id=store_id, user_id=current_user.id)

# 가게 좋아요 갯수 기능
@router.get('/{store_id}/likes/num', status_code=status.HTTP_204_NO_CONTENT)
def get_like_store(
        *,
        session: Session = Depends(get_session),
        store_id: int,
):
    return  service.get_like_num_store(session, store_id=store_id)


# 가게 좋아요 취소 기능
@router.delete('/{store_id}/likes', status_code=status.HTTP_204_NO_CONTENT)
def delete_like_store(
        *,
        session: Session = Depends(get_session),
        store_id: int,
        current_user: User = Depends(get_current_user)
):
    service.delete_like_store(session, store_id=store_id, user_id=current_user.id)

# 랜덤 메뉴
@router.get('/get/randomMenu', status_code=status.HTTP_204_NO_CONTENT)
def get_random_menu(
        *,
        session: Session = Depends(get_session),
):
    return  service.get_random_menu(session)