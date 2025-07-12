from fastapi import Depends,status,HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from api.utils.dependency import get_db
from api.models.stock import Stock