from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from api.utils.dependency import get_db
from api.responses.success_response import success_response
from api.services.indicator import indicator_service

indicator = APIRouter(prefix="/indicator", tags=['indicator'])

db_dependency = Annotated[Session,Depends(get_db)]

@indicator.get("/",status_code=status.HTTP_200_OK)
async def get_indicator(db: db_dependency):
    data = indicator_service.get_indicator(db)
    return success_response(
        message="지표들을 모두 출력합니다",
        data=data
    )

@indicator.post("/seed",status_code=status.HTTP_201_CREATED)
async def seed_indicator(db: db_dependency):
    indicator_service.seed_indicators(db)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="indicator seed"
    )

@indicator.put("/update",status_code=status.HTTP_200_OK)
async def update_indicator(db:db_dependency):
    indicator_service.update_prices(db)
    return success_response(
        message="가격과 등락률을 갱신합니다."
    )