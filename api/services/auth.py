import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from jose import jwt
from typing import Annotated
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from api.utils.dependency import get_db
from api.schemas.user import UserLogin, UserOut
from api.services.user import user_service
from api.models.refresh_token import RefreshToken

load_dotenv()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHMN = os.environ.get("ALGORITHM")
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
db_dependency = Annotated[Session,Depends(get_db)]

class AuthService:
    def handle_login(self, db : db_dependency, user_login : UserLogin, response : Response):
        user = user_service.get_user_by_email(db, user_login.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="등록된 이메일이 없습니다"
            )
        if not self.verify_password(user_login.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="비밀번호가 틀렸습니다"
            )
        access_token = self.create_access_token(user.id)
        refresh_token = self.create_refresh_token(user.id)

        db_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expiry_time=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        try: 
            db.add(db_token)
            db.commit()
            db.refresh(db_token)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="사용자 생성 중 오류가 발생했습니다"
            ) from e
        
        self.set_refresh_token_cookie(response, refresh_token)
        data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserOut.model_validate(user)
        }
        return data
    
    def verify_password(self, password: str, hashed_password) -> bool:
        return bcrypt_context.verify(password,hashed_password)
    
    def create_access_token(self, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMN)
    
    def create_refresh_token(self, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMN)
    
    def set_refresh_token_cookie(self, response: Response, token: str):
        response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * REFRESH_TOKEN_EXPIRE_DAYS,
        samesite="lax",
        secure=False 
    )
    
auth_service = AuthService()
