from pydantic import BaseModel

class StockBase(BaseModel):
    name : str
    ticker : str

class StockOut(StockBase):
    id : str

    class Config:
        from_attributes = True