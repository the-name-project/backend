from app.store.base import Service

from app.store.model import Store_Info, StoreLike
from sqlmodel import Session, select


class StoreService(Service[Store_Info]):
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


service = StoreService(Store_Info)

