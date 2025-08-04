import os
from dotenv import load_dotenv

import requests
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
import yfinance as ys

from api.utils.dependency import get_db
from api.schemas.feature import Featurein,FeatureOut
from api.services.stock import stock_service

load_dotenv()

db_dependency = Annotated[Session, Depends(get_db)]
AI_SERVER = os.environ.get("AI_SERVER")

class PredictService:
    def predict_stock(self, db: db_dependency, feature: Featurein, stock_id: str):
        data = self.get_feature(db,feature,stock_id)
        stock = stock_service.get_stock_id(db,stock_id)
        ai_data = self.predict_response(data)
        if not ai_data:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="예측값을 받아오지 못했습니다"
            )
        days = feature.period*3
        his_data = stock_service.get_price(stock.ticker, days)
        total_data = ai_data + his_data
        sorted_data = sorted(total_data,key=lambda x: x["date"])

        return sorted_data

    def get_feature(self, db: db_dependency, feature: Featurein, stock_id: str):
        stock = stock_service.get_stock_id(db,stock_id)
        ticker = stock.ticker
        value1 = self.convert_feature_to_int_value1(feature)
        value2 = feature.period
        return FeatureOut(
            string_value=ticker,
            int_value1=value1,
            int_value2=value2
        )
    def convert_feature_to_int_value1(self, feature: Featurein) -> str:
        bits = [
            int(feature.volume),
            int(feature.start),
            int(feature.high),
            int(feature.low),
            int(feature.fixed_rate),
            int(feature.per),
            int(feature.pbr),
            int(feature.psr),
            int(feature.snp),
            int(feature.roe),
            int(feature.roa),
            int(feature.opm),
            int(feature.npm)
        ]
        binary_string = ''.join(str(bit) for bit in bits)
        return binary_string
    
    def predict_response(self, feature: FeatureOut):
        try:
            response = requests.post(
                f"{AI_SERVER}/run-forecast",
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
                "date": item["ds"].split(" ")[0],  
                "data": item["TimeLLM"],
                "type": "predict"
            }
            for item in ai_data.get("forecast", [])
        ]

        return transformed
    
predict_service = PredictService()