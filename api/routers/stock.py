from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from typing import Annotated

from api.utils.dependency import get_db
from api.responses.success_response import success_response
from api.services.stock import stock_service

stock = APIRouter(prefix="/stock", tags=['stock'])

db_dependency = Annotated[Session,Depends(get_db)]

@stock.post("/saveSMP",status_code=status.HTTP_200_OK)
async def save_smp(db:db_dependency):
    stock_service.save_smp
    return success_response(
        message="SMP 500의 저장이 완료되었습니다"
    )