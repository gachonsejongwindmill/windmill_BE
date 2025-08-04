from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from api.models.user import User
from api.services.author import auth_service
from api.services.portfolio import portfolio_service
from api.schemas.avatar import AvatarIn,AvatarOut
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

@portfolio.post("/{avatar_id}", status_code=status.HTTP_200_OK)
async def portfolio_response(db: db_dependency, avatar_id: str):
    data = portfolio_service.portfolio_response(db, avatar_id)
    return success_response(
        message="포트폴리오를 출력합니다",
        data=data
    )

@portfolio.delete("/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_avatar(db: db_dependency):
    portfolio_service.delete_all_avatar(db)

    
@portfolio.delete("/{avatar_id}", status_code=status.HTTP_200_OK)
async def delete_avatar(db: db_dependency, avatar_id: str):
    portfolio_service.delete_avatar(db,avatar_id)
    return success_response(
        message=f"{avatar_id}를 삭제했습니다"
    )