from pydantic import BaseModel, ConfigDict

class AvatarIn(BaseModel):
    loss : int
    age : int

class AvatarOut(AvatarIn):
    id : str
    user_id : str

    model_config = ConfigDict(from_attributes=True)