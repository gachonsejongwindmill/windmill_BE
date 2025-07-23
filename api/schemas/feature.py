from pydantic import BaseModel, ConfigDict

class FeatureBase(BaseModel):
    ticker: str
    start: bool
    high: bool
    low: bool
    volume: bool
    fixed_rate: bool
    predict_range : int

class Featurein(FeatureBase):
    model_config = ConfigDict(from_attributes=True)

class FeatureOut(BaseModel):
    string_value: str
    int_value1: int
    int_value2: int