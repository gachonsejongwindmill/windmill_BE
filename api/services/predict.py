import os
from dotenv import load_dotenv

import requests
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from api.utils.dependency import get_db
from api.schemas.feature import Featurein,FeatureOut
from api.services.stock import stock_service

load_dotenv()

db_dependency = Annotated[Session, Depends(get_db)]
AI_SERVER = os.environ.get("AI_SERVER")

class PredictService:
    def predict_stock(self, db: db_dependency, feature: Featurein):
        data = self.get_feature(db,feature)
        ai_data = self.predict_response(data)
        
        return ai_data

    def get_feature(self, db: db_dependency, feature: Featurein):
        stock = stock_service.get_stock_id(db,feature.stock_id)
        ticker = stock.ticker
        value1 = self.convert_feature_to_int_value1(feature)
        value2 = feature.predict_range
        return FeatureOut(
            string_value=ticker,
            int_value1=value1,
            int_value2=value2
        )
       
    def convert_feature_to_int_value1(self, feature: Featurein) -> int:
        bits = [
            int(feature.volume),
            int(feature.start),
            int(feature.high),
            int(feature.low),
            int(feature.fixed_rate)
        ]
        binary_string = ''.join(str(bit) for bit in bits)
        return int(binary_string)
    
    def predict_response(self, feature: FeatureOut):
        try:
            response = requests.post(
                AI_SERVER,
                json={
                    "string_value": feature.string_value,
                    "int_value1": feature.int_value1,
                    "int_value2": feature.int_value2
                }
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ai 서버 연결에 실패했습니다"
            )
        
        ai_data = response.json()

        transformed = [
            {
                "date": item["ds"].split(" ")[0],  # 날짜만 추출
                "data": item["TimeLLM"]
            }
            for item in ai_data.get("forecast", [])
        ]

        return transformed
    
predict_service = PredictService()