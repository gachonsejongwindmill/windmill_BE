from pydantic import BaseModel, ConfigDict, field_validator
import datetime

class MyStockBase(BaseModel):
    id : str
    user_id : str
    stock_id : str
    average_cost : int
    all_stock_count : float

class MyStockAdd(BaseModel):
    buy_cost : int
    buy_stock_count : float
    date : datetime.date
    @field_validator("buy_cost","buy_stock_count")
    def no_zero(cls, v, info):
        if v == 0:
            raise ValueError("가격과 수량은 0이 될 수 없습니다.")
        return v


class MyStockOut(MyStockBase):
    buy_cost : int
    buy_stock_count : float
    date : datetime.date

    model_config = ConfigDict(from_attributes=True)

class MyStockListOut(MyStockBase):
    

    model_config = ConfigDict(from_attributes=True)


