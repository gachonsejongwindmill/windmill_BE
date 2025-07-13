from fastapi import Depends,status,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Annotated,List
import pandas as pd
import requests

from api.utils.dependency import get_db
from api.models.stock import Stock
from api.schemas.stock import StockBase,StockOut

db_dependency = Annotated[Session,Depends(get_db)]

class StockService:
    def save_stock_from_csv(self, db: Session, filepath: str = "data/sp500.csv"):
        try:
            df = pd.read_csv(filepath)

            if "Ticker" not in df.columns or "Name" not in df.columns:
                raise ValueError("CSV 파일에 Ticker 또는 Name 열이 없습니다.")

            for _, row in df.iterrows():
                ticker = str(row["Ticker"]).strip()
                name = str(row["Name"]).strip()

                if not ticker or not name:
                    continue

                stock = Stock(ticker=ticker, name=name)
                db.merge(stock)  # 중복된 ticker가 있으면 update, 없으면 insert

            db.commit()
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"S&P 500 저장 실패: {str(e)}"
            )
    
    def get_all_stock(self, db : db_dependency) -> List[StockOut]:
        stocks = db.query(Stock).order_by(Stock.ticker).all()
        return [StockOut.model_validate(stock) for stock in stocks]
    
    def get_stock_range(self, db : db_dependency, start : int, end : int):
        if start > end:
            raise HTTPException(status_code=400, detail="start 값은 end보다 작아야 합니다.")
        stocks = (
            db.query(Stock)
            .order_by(Stock.name)
            .offset(start - 1)
            .limit(end - start + 1)
            .all()
        )
        
        return [StockOut.model_validate(stock) for stock in stocks]
stock_service = StockService()