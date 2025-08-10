from pydantic import BaseModel

class IndicatorBase(BaseModel):
    name : str
    ticker : str
    current : float
    change_rate : float

class IndicatorOut(IndicatorBase):
    id : str
    class Config:
        from_attributes = True