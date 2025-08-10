from pydantic import BaseModel
from typing import Optional
class StockBase(BaseModel):
    name : str
    ticker : str
    price : Optional[float] = None
    change_rate : Optional[float] = None
class StockOut(StockBase):
    id : str
    class Config:
        from_attributes = True