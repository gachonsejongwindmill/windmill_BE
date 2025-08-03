from pydantic import BaseModel, ConfigDict

class AvartarIn(BaseModel):
    loss : int
    age : int

class AvartarOut(AvartarIn):
    id : str
    user_id : str

    model_config = ConfigDict(from_attributes=True)