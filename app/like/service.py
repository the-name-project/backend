from app.like.base import Service
from app.like.model import StoreLike
from fastapi.responses import JSONResponse
from sqlmodel import Session,select


class LikeService(Service[StoreLike]):
    # 가게 좋아요
    def like_store(self, session: Session, store_id: int, user_id: int) -> None:
        statement = (
            select(StoreLike)
            .where(StoreLike.store_id == store_id)
            .where(StoreLike.user_id == user_id)
        )
        store_like = session.exec(statement).one_or_none()
        if store_like:
            return

        store_like = StoreLike(store_id=store_id, user_id=user_id)
        session.add(store_like)
        session.commit()

    # 가게의 좋아요 갯수
    def get_like_num_store(self,session:Session,store_id:int)->None:
        statment = (
            select(StoreLike)
            .where(StoreLike.store_id == store_id)
        )
        
        store_like = session.exec(statment).all()
        
        if store_like is None:
            return None
        default = {
            'num' : len(store_like)
        }
        
        return JSONResponse(content=default)

    # 가게 좋아요 취소
    def delete_like_store(self, session: Session, store_id: int, user_id: int) -> None:
        statement = (
            select(StoreLike)
            .where(StoreLike.store_id == store_id)
            .where(StoreLike.user_id == user_id)
        )

        store_like = session.exec(statement).one_or_none()
        if store_like is None:
            return

        session.delete(store_like)
        session.commit()

service = LikeService(StoreLike)

