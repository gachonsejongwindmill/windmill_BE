from pydantic import BaseModel


class PortfolioOut(BaseModel):
    int_value1: int
    int_value2: int