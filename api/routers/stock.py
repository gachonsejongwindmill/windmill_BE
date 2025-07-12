from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from typing import Annotated

from api.utils.dependency import get_db
from api.responses.success_response import success_response
from api.services.stock import stock_service
from api.models.stock import Stock
from api.schemas.stock import StockOut

stock = APIRouter(prefix="/stock", tags=['stock'])

db_dependency = Annotated[Session,Depends(get_db)]


@stock.get("/",status_code=status.HTTP_200_OK)
async def get_all_stock(db:db_dependency):
    data = stock_service.get_all_stock(db)
    return success_response(
        message="모든 종목을 출력합니다",
        data=data
    )


@stock.post("/saveSMP",status_code=status.HTTP_200_OK)
async def save_smp(db:db_dependency):
    stock_service.save_stock_from_csv(db)
    return success_response(
        message="SMP 500의 저장이 완료되었습니다"
    )
