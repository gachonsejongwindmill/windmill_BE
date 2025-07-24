from fastapi import APIRouter,Depends, status
from typing import Annotated
from sqlalchemy.orm import Session

from api.responses.success_response import success_response
from api.utils.dependency import get_db
from api.services.predict import predict_service
from api.schemas.feature import Featurein

db_dependency = Annotated[Session, Depends(get_db)]

predict = APIRouter(prefix="/predict", tags=["predict"])

@predict.post("/{stock_id}",status_code=status.HTTP_200_OK)
async def predict_out(db: db_dependency, feature: Featurein, stock_id: str):
    data = predict_service.predict_stock(db,feature,stock_id)
    return success_response(
        message="예측된 값들을 출력합니다",
        data=data
    )