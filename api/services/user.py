import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated

from api.utils.dependency import get_db
from api.schemas.user import UserCreate
from api.models.user import User

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

db_dependency = Annotated[Session,Depends(get_db)]

class UserService:
    def create_user(self,user: UserCreate, db : db_dependency):
        if self.exist(db, user.email):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"이미 등록된 email입니다")
        hashed_password = bcrypt_context.hash(user.password)
        user.password = hashed_password
        user = User(**user.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        user = jsonable_encoder(
            self.get_user_detail(db=db,user_id=user.id),exclude={"password"}
        )

        return user

    def exist(self, db : db_dependency, email : str) -> bool:
        user = db.query(User).filter(User.email == email).first()

        if user:
            return True

        return False
    
    def get_user_detail(self, db : db_dependency, user_id : str):
        data = db.query(User).filter(User.id==user_id).first()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            ) 
        return data

    
    