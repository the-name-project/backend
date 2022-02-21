from fastapi import FastAPI, Depends, status, Query, APIRouter
from sqlmodel import Session, select
from app.DB_session import get_session
from typing import Optional, List

from app.review.service import service
from app.review.model import ReviewRead, ReviewCreate, ReviewUpdate
from app.user.exceptions import ForbiddenException
from app.user.router import get_current_user
from app.user.model import User

router = APIRouter()


# 가게 리뷰 조회
@router.get('/store', response_model=List[ReviewRead], status_code=status.HTTP_200_OK)
def read_review(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=100, limit=100),
):
    return service.find_all(session, offset=offset, limit=limit)


# 가게 리뷰 생성
@router.post('/create/store/{store_id}', status_code=status.HTTP_201_CREATED)
def create_review(
        *,
        session: Session = Depends(get_session),
        store_id: int,
        review_data: ReviewCreate,
        current_user: User = Depends(get_current_user),
):
    return service.review_store(
        session,
        object_data=review_data,
        store_id=store_id,
        user_id=current_user.id
    )


# 가게 리뷰 수정
@router.patch('/{review_id}', response_model=ReviewRead, status_code=status.HTTP_200_OK)
def update_review(
        *,
        session: Session = Depends(get_session),
        review_id: int,
        review_body: ReviewUpdate,
        current_user: User = Depends(get_current_user),
):
    review = service.find_one(session, id=review_id)
    # if not article:
    #     raise ArticleNotFoundException
    if review.user_id != current_user.id:
        raise ForbiddenException(detail="Not allowed to update this review.")
    return service.update(session, model_object=review, object_data=review_body)


# 가게 리뷰 삭제
@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
        *,
        session: Session = Depends(get_session),
        review_id: int,
        current_user: User = Depends(get_current_user),
):
    review = service.find_one(session, id=review_id)
    if review.user_id != current_user.id:
        raise ForbiddenException(detail="Not allowed to update this review.")
    return service.remove(session, model_object=review)

