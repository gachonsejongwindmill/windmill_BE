from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.models.user import User
from api.models.avatar import Avatar
from api.services.author import auth_service
from api.schemas.avatar import AvatarIn,AvatarOut
from api.utils.dependency import get_db

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]

class PortfolioService:
    def add_avatar(self, user: user_dependency, db: db_dependency, avatar: AvatarIn):
        user_avatar = Avatar(
            user_id = user.id,
            age = avatar.age,
            loss = avatar.loss
        )

        try:
            db.add(user_avatar)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="아바타 생성 중 오류가 발생하였습니다"
            )
        
        return AvatarOut.model_validate(user_avatar)
    
    def get_avatar(self, user: user_dependency, db: db_dependency):
        datas = db.query(Avatar).filter(Avatar.user_id == user.id).all()
        return [AvatarOut.model_validate(data) for data in datas]

portfolio_service = PortfolioService()