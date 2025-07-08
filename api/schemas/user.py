from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Literal,Optional


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=10)
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