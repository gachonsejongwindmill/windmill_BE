from pydantic import BaseModel

class Feature(BaseModel):
    start: bool
    end: bool
    high: bool
    low: bool
    volume: bool
    fixed_rate: bool