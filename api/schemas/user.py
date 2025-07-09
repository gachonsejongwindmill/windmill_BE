from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Literal,Optional


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=10,regex="^[가-힣a-zA-Z0-9]+$")
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: str

    class Config:
        from_attributes = True