from pydantic import BaseModel

class AvartarIn(BaseModel):
    loss : str
    age : str
class AvartarOut(AvartarIn):
    id : str
    user_id : str