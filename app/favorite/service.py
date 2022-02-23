from app.favorite.base import Service
from app.favorite.model import  StoreFavorite
from app.store.model import Store_Info
from sqlmodel import Session, select
from fastapi.responses import JSONResponse


class FavoriteService(Service[Store_Info]):
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
        statment = (
            select(StoreFavorite)
            .where(StoreFavorite.user_id == user_id)
        )
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
            if store:
                default.append(store.dict())
        return JSONResponse(content=default)
        

    # 가게 찜 취소
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

service = FavoriteService(Store_Info)

