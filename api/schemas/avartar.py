from pydantic import BaseModel, ConfigDict

class AvartarIn(BaseModel):
    loss : str
    age : str

class AvartarOut(AvartarIn):
    id : str
    user_id : str
    
    model_config = ConfigDict(from_attributes=True)