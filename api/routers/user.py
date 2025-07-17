from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from typing import Annotated

from api.utils.dependency import get_db
from api.models.user import User
from api.responses.success_response import success_response
from api.services.user import user_service
from api.services.auth import auth_service

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

@user.post("/interest/{stock_id}",status_code=status.HTTP_201_CREATED)
async def add_interest(stock_id: str, user: user_dependency, db: db_dependency):
    interest = user_service.user_interest(user,db,stock_id)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="즐겨찾기에 추가합니다",
        data=interest
    )