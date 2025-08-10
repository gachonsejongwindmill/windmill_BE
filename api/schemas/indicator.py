from pydantic import BaseModel
from typing import Optional
class IndicatorBase(BaseModel):
    name : str
    ticker : str
    current : Optional[float] = None
    change_rate : Optional[float] = None

class IndicatorOut(IndicatorBase):
    id : str
    class Config:
        from_attributes = True