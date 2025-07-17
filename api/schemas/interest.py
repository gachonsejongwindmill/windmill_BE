from pydantic import BaseModel, ConfigDict

class InterestOut(BaseModel):
    id: str
    user_id: str
    stock_id: str
    interested: bool

    model_config = ConfigDict(from_attributes=True)