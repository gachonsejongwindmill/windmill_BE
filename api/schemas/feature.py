from pydantic import BaseModel, ConfigDict

class FeatureBase(BaseModel):
    start: bool
    high: bool
    low: bool
    volume: bool
    fixed_rate: bool
    period : int

class Featurein(FeatureBase):
    stock_id: str
    model_config = ConfigDict(from_attributes=True)

class FeatureOut(BaseModel):
    string_value: str
    int_value1: str
    int_value2: int