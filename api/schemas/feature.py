from pydantic import BaseModel, ConfigDict

class FeatureBase(BaseModel):
    start: bool
    high: bool
    low: bool
    volume: bool
    fixed_rate: bool
    per: bool
    pbr: bool
    psr: bool
    snp: bool
    roe: bool
    roa: bool
    opm: bool
    npm: bool
    period : int

class Featurein(FeatureBase):
    stock_id: str
    model_config = ConfigDict(from_attributes=True)

class FeatureOut(BaseModel):
    string_value: str
    int_value1: str
    int_value2: int