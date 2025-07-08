from fastapi import APIRouter, Depends, status, Response, Request
from sqlalchemy.orm import Session

from api.responses.success_response import success_response
from api.services.user import user_service
from api.services.auth import auth_service
from api.schemas.user import UserCreate,UserLogin
from api.utils.dependency import get_db


auth = APIRouter(prefix="/auth", tags=['auth'])

@auth.post("/register",status_code=status.HTTP_201_CREATED)
async def user_register(user: UserCreate, db : Session = Depends(get_db)):
    data = user_service.create_user(user,db)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="유저가 성공적으로 생성됐습니다.",
        data=data
    )

@auth.post("/login",status_code=status.HTTP_200_OK)
async def user_login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    data = auth_service.handle_login(db, user, response)

    return success_response(
        message="유저가 성공적으로 로그인했습니다.",
        data=data
    )

@auth.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    auth_service.handle_logout(db, request, response)
    return success_response(message="로그아웃 되었습니다.")