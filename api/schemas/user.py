from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Literal,Optional


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

