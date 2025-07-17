from pydantic import BaseModel

class InterestOut(BaseModel):
    id: str
    user_id: str
    stock_id: str
    interested: bool

    class Config:
        orm_mode = True