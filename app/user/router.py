from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session

from .service import service
from .schemas import Token
from .service import create_access_token, get_current_user
from .exceptions import UserEmailAlreadyExistsException, UserNotFoundException
from .model import User, UserCreate, UserRead, UserUpdate
from .exceptions import ForbiddenException
from app.DB_session import get_session

from sqlalchemy.exc import IntegrityError


router = APIRouter()

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    session: Session = Depends(get_session),
    user_body: UserCreate,
) -> Any:
    try:
        return service.create(session, object_in=user_body)
    except IntegrityError:
        raise UserEmailAlreadyExistsException()


@router.get("", response_model=List[UserRead], status_code=status.HTTP_200_OK)
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> Any:
    return service.find_all(session, offset=offset, limit=limit)


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
) -> Any:
    user = service.find_one(session, user_id)
    if not user:
        raise UserNotFoundException()

    return user


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user_body: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    user = service.find_one(session, user_id)
    if not user:
        raise UserNotFoundException()
    if user.id != current_user.id:
        raise ForbiddenException()

    return service.update(session, object_model=user, object_in=user_body)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
) -> Any:
    user = service.find_one(session, user_id)
    if not user:
        raise UserNotFoundException()

    service.remove(session, object_model=user)


@router.post("/token", response_model=Token, status_code=200)
def authenticate(
    *,
    session: Session = Depends(get_session),
    data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = service.authenticate(session, email=data.username, password=data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@router.get("/token", response_model=User, status_code=200)
def test_token(current_user: User = Depends(get_current_user)) -> Any:
    return current_user
