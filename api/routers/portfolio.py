from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from api.models.user import User
from api.services.author import auth_service
from api.services.portfolio import portfolio_service
from api.schemas.avartar import AvatarIn,AvatarOut
from api.responses.success_response import success_response
from api.utils.dependency import get_db

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]

portfolio = APIRouter(prefix="/portfolio", tags=["portfolio"])

@portfolio.get("/avatar", status_code=status.HTTP_200_OK)
async def get_avartar(db: db_dependency, user: user_dependency):
    data = portfolio_service.get_avatar(user, db)
    return success_response(
        message="아바타를 불러옵니다",
        data=data
    )

@portfolio.post("/avatar", status_code=status.HTTP_200_OK)
async def add_avatar(db: db_dependency, user: user_dependency, avartar: AvatarIn):
    data = portfolio_service.add_avatar(user,db,avartar)
    return success_response(
        message="아바타를 생성합니다",
        data=data
    )


