from pydantic import BaseModel

class StockBase(BaseModel):
    name : str
    ticker : str
    price : float
    change_rate : float
class StockOut(StockBase):
    id : str
    class Config:
        from_attributes = True