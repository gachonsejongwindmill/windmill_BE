from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.responses.success_response import success_response
from api.services.user import user_service
from api.schemas.user import UserCreate
from api.utils.dependency import get_db


auth = APIRouter(prefix="/auth", tags=['auth'])

@auth.post("/register",status_code=status.HTTP_201_CREATED)
async def user_register(user: UserCreate, db : Session = Depends(get_db)):
    data = user_service.create_user(user,db)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=data
    )