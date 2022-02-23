import json
from random import randint
from app.store.base import Service
from app.store.model import Store, StoreLike
from app.store.menu.model import Menu
from sqlmodel import Session, select
from fastapi.responses import JSONResponse
from typing import List
from sqlmodel import Session,select
from fastapi.exceptions import HTTPException
from fastapi import Query, status
import pandas as pd

class StoreService(Service[Store]):
    #가게 필터
    def filter_store(self,session:Session,skip:int,limit:int,wheres:List[str]=Query(None)) -> None:
        first = 0
        end = skip
        filtered = pd.DataFrame()
        
        while limit>len(filtered.index):
            first = end
            end=first+100
            Statement = select(Store).offset(first).limit(100)
            data_info = session.exec(Statement).all()
            
            if data_info == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if len(data_info) == 0:
                break
            df = []
            
            for  data in data_info:
                df.append(data.__dict__)
            df = pd.DataFrame(df)
            if wheres:
                for where in wheres:
                    df= df[df['address'].str.contains(where)]
            else:
                pass
            if len(filtered.index) ==0:
                filtered = df
            else:
                filtered = pd.concat([filtered,df])
            if len(filtered.index) > limit:
                
                while len(filtered.index) != limit:
                    end=  int(filtered.iloc[len(filtered.index)-1].id)
                    filtered = filtered[:-1]
        default = []
        
        for i in range(0,len(filtered.index)):
            which  = filtered.iloc[i].id
            Statement = select(Store).where(Store.id == int(which))
            data_info = session.exec(Statement).first()
            print(data_info)
            if data_info:
                default.append(data_info.dict())
        default.append({
            "end" : {end},
            "amount": {len(filtered.index)}
        })
        
        return default

    #가게 필터 (네이버 평점순)
    def filter_store_naver(self,session:Session,skip:int,limit:int,wheres:List[str]=Query(None)) -> None:
        first = 0
        end = skip
        filtered = pd.DataFrame()
        
        while limit>len(filtered.index):
            first = end
            end=first+100
            Statement = select(Store).where(Store.naver_score != "None").order_by(Store.naver_score.desc()).offset(first).limit(100)
            data_info = session.exec(Statement).all()
            
            if data_info == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if len(data_info) == 0:
                break
            df = []
            
            for  data in data_info:
                df.append(data.__dict__)
            df = pd.DataFrame(df)
            if wheres:
                for where in wheres:
                    df= df[df['address'].str.contains(where)]
            else:
                pass
            if len(filtered.index) ==0:
                filtered = df
            else:
                filtered = pd.concat([filtered,df])
            if len(filtered.index) > limit:
                
                while len(filtered.index) != limit:
                    end=  int(filtered.iloc[len(filtered.index)-1].id)
                    filtered = filtered[:-1]
        default = []
        filtered = filtered.sort_values(by='naver_score' ,ascending=False)
        for i in range(0,len(filtered.index)):
            which  = filtered.iloc[i].id
            Statement = select(Store).where(Store.id == int(which))
            data_info = session.exec(Statement).first()
            default.append(data_info.dict())
        default.append({
            "end" : {end},
            "amount": {len(filtered.index)}
        })
        
        return default

    # 가게 필터 (카카오 평점순)
    def filter_store_kakao(self,session:Session,skip:int,limit:int,wheres:List[str]=Query(None))->None:
        first = 0
        end = skip
        filtered = pd.DataFrame()
        
        while limit>len(filtered.index):
            first = end
            end=first+100
            Statement = select(Store).where(Store.daum_score != "None").order_by(Store.daum_score.desc()).offset(first).limit(100)
            data_info = session.exec(Statement).all()
            
            if data_info == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            if len(data_info) == 0:
                break
            df = []
            
            for  data in data_info:
                df.append(data.__dict__)
            df = pd.DataFrame(df)
            if wheres:
                for where in wheres:
                    df= df[df['address'].str.contains(where)]
            else:
                pass
            if len(filtered.index) ==0:
                filtered = df
            else:
                filtered = pd.concat([filtered,df])
            if len(filtered.index) > limit:
                
                while len(filtered.index) != limit:
                    end=  int(filtered.iloc[len(filtered.index)-1].id)
                    filtered = filtered[:-1]
        default = []
        filtered = filtered.sort_values(by='daum_score' ,ascending=False)
        for i in range(0,len(filtered.index)):
            which  = filtered.iloc[i].id
            Statement = select(Store).where(Store.id == int(which))
            data_info = session.exec(Statement).first()
            default.append(data_info.dict())
        default.append({
            "end" : {end},
            "amount": {len(filtered.index)}
        })
        
        return default

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
    
    #랜덤 메뉴
    def get_random_menu(self,session:Session) -> None:
        statement = (
            select(Menu)
            .where(Menu.menu_image != "None")
        )
        random_menu = session.exec(statement).all()
        if random_menu is None:
            return None
        RandomNum = randint(1,len(random_menu))
        default = random_menu[RandomNum-1].dict()
        return JSONResponse(content=default)
        

   

service = StoreService(Store)

