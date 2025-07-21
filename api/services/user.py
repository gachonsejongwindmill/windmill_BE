import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session, aliased
from passlib.context import CryptContext
from typing import Annotated, Optional
import datetime

from api.utils.dependency import get_db
from api.schemas.user import UserCreate, UserOut
from api.schemas.mystock import MyStockAdd,MyStockOut,MyStockListOut
from api.schemas.interest import InterestOut
from api.models.user import User
from api.models.stock import Stock
from api.models.interest import Interest
from api.models.mystock import MyStock
from api.services.author import auth_service

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]
class UserService:
    def create_user(self,user_create: UserCreate, db : db_dependency):
        
        if self.email_exist(db, user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다."
            )
        hashed_password = bcrypt_context.hash(user_create.password)
        
        user = User(
            email=user_create.email,
            username=user_create.username,
            password=hashed_password
        )
        try: 
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="사용자 생성 중 오류가 발생했습니다"
            ) from e



        user = jsonable_encoder(
            self.get_user_detail(db=db,user_id=user.id),exclude={"password"}
        )

        return UserOut.model_validate(user)

    def email_exist(self, db : db_dependency, email : str) -> bool:
        return db.query(User).filter(User.email == email).first() is not None
    
    def get_user_detail(self, db : db_dependency, user_id : str):
        user = db.query(User).filter(User.id==user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="해당 유저를 찾을 수 없습니다."
            ) 
        return UserOut.model_validate(user)
   
    def get_user_by_email(self, db: db_dependency, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_all_users(self, db: db_dependency) -> Optional[User]:
        users = db.query(User).all()
        return [UserOut.model_validate(user) for user in users]
    
    def user_interest(self, user: user_dependency, db: db_dependency, stock_id : str):
        stock = db.query(Stock).filter(Stock.id == stock_id).first()

        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 종목이 존재하지 않습니다."
            )
        
        existing = db.query(Interest).filter(
            and_(
                Interest.user_id == user.id,
                Interest.stock_id == stock_id
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 관심 종목으로 등록되어 있습니다."
            )


        interest = Interest(
            user_id=user.id,
            stock_id=stock_id,
            interested=True
        )
        try:
            db.add(interest)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="즐겨찾기 추가 중 오류가 발생하였습니다"
            )
        
        return InterestOut.model_validate(interest)
   
    def get_all_user_interest(self, user: user_dependency, db: db_dependency) -> Optional[Interest]:
        interests = db.query(Interest).filter(Interest.user_id==user.id).all()
        return [InterestOut.model_validate(interest) for interest in interests]
    
    def delete_interest(self, user: user_dependency, db: db_dependency, stock_id:str):
        interest = db.query(Interest).filter(Interest.user_id==user.id, Interest.stock_id==stock_id).first()
        if not interest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="등록된 interest가 없습니다"
            )
        db.delete(interest)
        db.commit()

    def add_mystock(self, user: user_dependency, db: db_dependency, stock_id: str, input: MyStockAdd):
        stock = db.query(Stock).filter(Stock.id==stock_id).first()
        cost = 0
        count = 0
        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 종목이 존재하지 않습니다."
            )
        mystock = (
            db.query(MyStock)
            .filter(MyStock.user_id==user.id, MyStock.stock_id == stock.id)
            .order_by(desc(MyStock.created_at))
            .first()
        )
        if mystock:
            cost = mystock.average_cost
            count = mystock.all_stock_count
        if input.buy_stock_count > 0:
            result =int(((cost*count)+(input.buy_cost*input.buy_stock_count))/(count+input.buy_stock_count))
        else:
            if count+input.buy_stock_count<0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="보유하신 수량보다 많이 팔 수 없습니다"
                )
            elif count+input.buy_stock_count == 0:
                result = 0
            else: result = cost
            
        mystockadd = MyStock(
            user_id = user.id,
            stock_id = stock.id,
            average_cost = result,
            all_stock_count = input.buy_stock_count + count,
            buy_cost = input.buy_cost,
            buy_stock_count = input.buy_stock_count,
            date = input.date
        )
        try:
            db.add(mystockadd)
            db.commit()
            db.refresh(mystockadd)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="보유주식 추가 중 오류가 발생하였습니다"
            )
        
        return MyStockOut.model_validate(mystockadd)
    
    def get_mystock(self, user: user_dependency, db: db_dependency, stock_id: str):
        mystocks = db.query(MyStock).filter(MyStock.user_id==user.id, MyStock.stock_id == stock_id).order_by(desc(MyStock.date)).all()
        return [MyStockOut.model_validate(mystock) for mystock in mystocks]
    
    def get_mystock_list(self, user: user_dependency, db: db_dependency):
        subquery = (
            db.query(
                MyStock.stock_id,
                func.max(MyStock.date).label("latest_date")
            )
            .filter(MyStock.user_id == user.id)
            .group_by(MyStock.stock_id)
            .subquery()
        )

        latest_stocks = (
            db.query(MyStock)
            .join(
                subquery,
                (MyStock.stock_id == subquery.c.stock_id) & (MyStock.date == subquery.c.latest_date)
            )
            .filter(MyStock.user_id == user.id)
            .all()
        )

        return [MyStockListOut.model_validate(ms) for ms in latest_stocks]


        

user_service = UserService()
    
