from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum
from api.models.abstract import AbstractBaseModel



class User(AbstractBaseModel):
    __tablename__ = 'user'
    username : Mapped[str]
    email : Mapped[str] = mapped_column(unique=True)
    password : Mapped[str] = mapped_column(nullable=False)
    
    refresh_token = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    def __str__(self) -> str:
        return self.username
