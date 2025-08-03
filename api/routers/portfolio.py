from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from api.models.user import User
from api.services.author import auth_service
from api.services.portfolio import portfolio_service
from api.schemas.avartar import AvartarIn,AvartarOut
from api.responses.success_response import success_response
from api.utils.dependency import get_db

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]

portfolio = APIRouter(prefix="/portfolio", tags=["portfolio"])

@portfolio.post("/avartar", status_code=status.HTTP_200_OK)
async def add_avartar(db: db_dependency, user: user_dependency, avartar: AvartarIn):
    data = portfolio_service.add_avartar(user,db,avartar)
    return success_response(
        message="아바타를 생성합니다",
        data=data
    )


