from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from typing import Annotated

from api.utils.dependency import get_db
from api.models.user import User
from api.responses.success_response import success_response
from api.services.user import user_service
from api.services.author import auth_service
from api.schemas.mystock import MyStockAdd

user = APIRouter(prefix="/user", tags= ['user'])

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]

@user.get("/",status_code=status.HTTP_200_OK)
async def get_app_user(db: db_dependency):
    data = user_service.get_all_users(db)
    return success_response(
        message="유저 목록을 반환합니다",
        data=data
    )


@user.get("/interest",status_code=status.HTTP_200_OK)
async def get_interest(user: user_dependency, db: db_dependency):
    data = user_service.get_all_user_interest(user,db)
    return success_response(
        message="즐겨찾기 목록을 반환합니다",
        data=data
    )

@user.get("/mystock",status_code=status.HTTP_200_OK)
async def get_mystock(user: user_dependency, db: db_dependency):
    data = user_service.get_mystock(user,db)
    return success_response(
        message="내 주식 목록을 반환합니다",
        data = data
    )

@user.get("/mystock/{stock_id}", status_code=status.HTTP_200_OK)
async def get_mystock_list(user: user_dependency, db: db_dependency, stock_id : str):
    data = user_service.get_mystock_list(user, db, stock_id)
    return success_response(
        message=f"{stock_id}의 로그를 출력합니다",
        data=data
    )

@user.post("/interest/{stock_id}",status_code=status.HTTP_201_CREATED)
async def add_interest(stock_id: str, user: user_dependency, db: db_dependency):
    interest = user_service.user_interest(user,db,stock_id)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="즐겨찾기에 추가합니다",
        data=interest
    )

@user.post("/mystock/{stock_id}",status_code=status.HTTP_201_CREATED)
async def add_mystock(stock_id: str, user: user_dependency, db: db_dependency, input : MyStockAdd):
    mystock = user_service.add_mystock(user, db, stock_id, input)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="my stock에 추가합니다",
        data = mystock
    )


@user.delete("/interest/{stock_id}", status_code=status.HTTP_200_OK)
async def delete_interest(stock_id: str, user: user_dependency, db: db_dependency):
    user_service.delete_interest(user,db,stock_id)
    return success_response(
        status_code=status.HTTP_200_OK,
        message="즐겨찾기 목록에 삭제 되었습니다"
    )