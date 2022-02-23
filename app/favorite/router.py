from sqlmodel import Session
from fastapi import APIRouter, Depends, status

from app.DB_session import get_session
from app.user.model import User
from app.user.service import get_current_user
from app.favorite.service import service

router = APIRouter()


# 가게 찜 기능
@router.post('/do', status_code=status.HTTP_204_NO_CONTENT)
def do_favorite_store(
        *,
        session: Session = Depends(get_session),
        store_id: int,
        current_user: User = Depends(get_current_user)
):
    
    service.favorite_store(session, store_id=store_id, user_id=current_user.id)

# 유저의 찜 가게
@router.post('/get/user', status_code=status.HTTP_204_NO_CONTENT)
def get_favorite_store(
        *,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return service.get_favorite_store(session, user_id=current_user.id)

# 가게 찜 취소 기능
@router.delete('/del', status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite_store(
        *,
        session: Session = Depends(get_session),
        store_id: int,
        current_user: User = Depends(get_current_user)
):
    service.delete_favorite_store(session, store_id=store_id, user_id=current_user.id)

# 가게 찜 갯수 기능
@router.post('/get/store/num', status_code=status.HTTP_204_NO_CONTENT)
def get_favorite_num_store(
        *,
        session: Session = Depends(get_session),
        store_id: int,
):
    return  service.get_favorite_store_num(session, store_id=store_id)