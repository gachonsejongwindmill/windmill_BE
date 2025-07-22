from pydantic import BaseModel, ConfigDict

class FeatureBase(BaseModel):
    start: bool
    end: bool
    high: bool
    low: bool
    volume: bool
    fixed_rate: bool

class FeatureOut(FeatureBase):
    ticker: str
    model_config = ConfigDict(from_attributes=True)