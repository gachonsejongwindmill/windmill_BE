from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum
from api.models.abstract import AbstractBaseModel



class User(AbstractBaseModel):
    __tablename__ = 'user'
    username : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str] = mapped_column(unique=True)
    password : Mapped[str] = mapped_column(nullable=False)
    
    def __str__(self) -> str:
        return self.username
