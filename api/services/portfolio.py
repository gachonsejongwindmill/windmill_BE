import os
from dotenv import load_dotenv

import requests
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.models.user import User
from api.models.avatar import Avatar
from api.services.author import auth_service
from api.services.stock import stock_service
from api.schemas.avatar import AvatarIn,AvatarOut
from api.schemas.portfolio import PortfolioOut
from api.utils.dependency import get_db

load_dotenv()

AI_SERVER = os.environ.get("AI_SERVER")
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]

class PortfolioService:
    ## 아바타 서비스
    ## 
    ##

    def add_avatar(self, user: user_dependency, db: db_dependency, avatar: AvatarIn):
        user_avatar = Avatar(
            name = avatar.name,
            user_id = user.id,
            age = avatar.age,
            loss = avatar.loss
        )

        try:
            db.add(user_avatar)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="아바타 생성 중 오류가 발생하였습니다"
            )
        
        return AvatarOut.model_validate(user_avatar)
    
    def get_avatar(self, user: user_dependency, db: db_dependency):
        datas = db.query(Avatar).filter(Avatar.user_id == user.id).all()
        return [AvatarOut.model_validate(data) for data in datas]
    
    def delete_all_avatar(self, db: db_dependency):
        avatar = db.query(Avatar).delete()
        db.commit()
    
    def delete_avatar(self, db: db_dependency, avatar_id: str):
        avatar = db.query(Avatar).filter(Avatar.id==avatar_id).first()
        db.delete(avatar)
        db.commit()


    ## 포트폴리오 서비스
    ##
    ##

    def portfolio_response(self, db: db_dependency, avatar_id: str):
        avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
        if not avatar:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="아바타가 존재하지 않습니다"
            )
        value = AvatarOut.model_validate(avatar)
        try:
            response = requests.post(
                f"{AI_SERVER}/run-predict",
                json={
                    "int_value1":value.loss,
                    "int_value2":value.age
                }
                
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ai 서버 연결에 실패했습니다"
            )
        
        ai_data = response.json()
        transformed = self.transform_data(db,ai_data)

        return transformed

        
    def transform_data(self,db: db_dependency, data):
        data1 = data.get("result",{})
        data2 = data.get("result2",{})
        
        transformed_result1 = []
        for ticker, result_value in data1.items():
            stock_id = stock_service.get_stock_id_by_ticker(db, ticker)
            if not stock_id:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{ticker}를 찾을 수 없습니다"
                )
            forecast_list = data2.get(ticker,[])
            forecast = [
                {
                    "data": item["y"],
                    "date": item["ds"],
                    "type": "predict"
                }
                for item in forecast_list
            ]
            his_data = stock_service.get_price(ticker,90)
            total_data = his_data+forecast
            total_data.sort(key=lambda x: x["date"])
            
            transformed_result1.append({
                "stockId": stock_id,
                "ticker": ticker,
                "ratio": result_value[0],
                "returnRate": result_value[1],
                "avgRoc": result_value[2],
                "graph": total_data
            })

        transformed_result2=[
            {
                "date": item["ds"],  
                "data": item["y"]
            }
            for item in data.get("result3", [])
        ]

        transformed = {
            "result":transformed_result1,
            "result2":transformed_result2
        }

        return transformed





        
        

portfolio_service = PortfolioService()