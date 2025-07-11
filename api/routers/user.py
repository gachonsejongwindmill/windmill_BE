from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from typing import Annotated

from api.utils.dependency import get_db
from api.responses.success_response import success_response
from api.services.user import user_service

user = APIRouter(prefix="/user", tags= ['user'])

db_dependency = Annotated[Session,Depends(get_db)]

@user.get("/",status_code=status.HTTP_200_OK)
async def get_app_user(db: db_dependency):
    data = user_service.get_all_users(db)
    return success_response(
        message="유저 목록을 반환합니다",
        data=data
    )