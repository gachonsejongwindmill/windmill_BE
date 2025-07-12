from fastapi import Depends,status,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Annotated
import pandas as pd

from api.utils.dependency import get_db
from api.models.stock import Stock
from api.schemas.stock import StockBase,StockOut

db_dependency = Annotated[Session,Depends(get_db)]

class StockService:
    def save_smp(self, db : db_dependency):
        wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        df = pd.read_html(wiki_url)[0]

        symbols = df['Symbol'].tolist()
        names = df['Security'].tolist()

        for symbol, name in zip(symbols, names):
            stock = Stock(ticker=symbol, name=name)
            db.merge(stock)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"DB 저장 중 오류 발생: {str(e)}"
            )
        
stock_service = StockService()