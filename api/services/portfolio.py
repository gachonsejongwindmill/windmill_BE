from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from api.models.user import User
from api.models.avartar import Avartar
from api.services.author import auth_service
from api.schemas.avartar import AvartarIn,AvartarOut
from api.utils.dependency import get_db

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[User,Depends(auth_service.get_current_user)]

class PortfolioService:
    def add_avartar(self, user: user_dependency, db: db_dependency, avartar: AvartarIn):
        user_avartar = Avartar