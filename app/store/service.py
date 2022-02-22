
from app.store.base import Service

from app.store.model import Store_Info, StoreLike, StoreFavorite
from sqlmodel import Session, select
from fastapi.responses import JSONResponse



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

    # 가게의 좋아요 갯수
    def get_like_store(self,session:Session,store_id:int)->None:
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
    
    # 가게 찜
    def favorite_store(self, session: Session, store_id: int, user_id: int) -> None:
        statement = (
            select(StoreFavorite)
            .where(StoreFavorite.store_id == store_id)
            .where(StoreFavorite.user_id == user_id)
        )
        store_favorite = session.exec(statement).one_or_none()
        if store_favorite:
            return

        store_favorite = StoreFavorite(store_id=store_id, user_id=user_id)
        session.add(store_favorite)
        session.commit()

    # 유저가 찜한 가게
    def get_favorite_store(self,session:Session,user_id:int)->None:
        print("="*100)
        statment = (
            select(StoreFavorite)
            .where(StoreFavorite.user_id == user_id)
        )
        print("="*100)
        store_favorite = session.exec(statment).all()
        
        print(store_favorite)
        if store_favorite is None:
            return None
        
        default = []
        for favorite in store_favorite:
            store_statment=(
                select(Store_Info)
                .where(Store_Info.id == favorite.store_id)
            )
            store = session.exec(store_statment).first()
            print(type(store))
            if store:
                default.append(store.dict())
        return JSONResponse(content=default)
        

    # 가게 좋아요 취소
    def delete_favorite_store(self, session: Session, store_id: int, user_id: int) -> None:
        statement = (
            select(StoreFavorite)
            .where(StoreFavorite.store_id == store_id)
            .where(StoreFavorite.user_id == user_id)
        )

        store_favorite = session.exec(statement).one_or_none()
        if store_favorite is None:
            return

        session.delete(store_favorite)
        session.commit()

    # 가게의 찜 갯수
    def get_favorite_store_num(self,session:Session,store_id:int)->None:
        statment = (
            select(StoreFavorite)
            .where(StoreFavorite.store_id == store_id)
        )
        
        store_favorite = session.exec(statment).all()
        
        if store_favorite is None:
            return None
        default = {
            'num' : len(store_favorite)
        }
        
        return JSONResponse(content=default)

service = StoreService(Store_Info)

