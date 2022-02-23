from sqlmodel import Session,select
from fastapi import APIRouter, Depends, Query, status

from app.DB_session import get_session
from app.user.model import User
from app.user.service import get_current_user
from app.store.service import service

router = APIRouter()

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