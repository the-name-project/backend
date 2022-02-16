from typing import Optional, Any, Union

from sqlmodel import Session, select

import secrets

from app.base import Service

from .security import get_password_hash, verify_password
from .model import User, UserCreate, UserUpdate
from .exceptions import UserNotFoundException
from .schemas import TokenPayload
from app.DB_session import get_session

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError


ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=60
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secrets.token_urlsafe(32), algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, secrets.token_urlsafe(32), algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = service.find_one(session, id=token_data.sub)
    if not user:
        raise UserNotFoundException()

    return user


class UserService(Service[User, UserCreate, UserUpdate]):
    def create(self, session: Session, *, object_in: UserCreate) -> User:
        object_in.hashed_password = get_password_hash(object_in.hashed_password)
        user = User.from_orm(object_in)

        session.add(user)
        session.commit()

        session.refresh(user)
        return user

    def update(
        self,
        session: Session,
        *,
        object_model: User,
        object_in: UserUpdate,
    ) -> User:
        if object_in.hashed_password:
            object_in.hashed_password = get_password_hash(object_in.hashed_password)

        return super().update(session, object_model=object_model, object_in=object_in)

    def authenticate(
        self, session: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user


service = UserService(User)
