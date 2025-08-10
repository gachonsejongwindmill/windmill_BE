from fastapi import Depends,status,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Annotated,List, Optional, Iterable, List, Dict
import pandas as pd
import requests
import yfinance as ys
from decimal import Decimal, ROUND_HALF_UP

from api.utils.dependency import get_db
from api.models.stock import Stock
from api.models.interest import Interest
from api.schemas.stock import StockBase,StockOut
from api.schemas.interest import InterestOut

db_dependency = Annotated[Session,Depends(get_db)]


def _chunked(iterable: Iterable[str], size: int) -> List[List[str]]:
    buf, out = [], []
    for x in iterable:
        buf.append(x)
        if len(buf) == size:
            out.append(buf)
            buf = []
    if buf:
        out.append(buf)
    return out

def _to_decimal(value: float | None, q: str = "0.01") -> Decimal | None:
    if value is None:
        return None
    try:
        return (Decimal(str(value))).quantize(Decimal(q), rounding=ROUND_HALF_UP)
    except Exception:
        return None


class StockService:
    def save_stock_from_csv(self, db: Session, filepath: str = "data/sp500.csv"):
        try:
            df = pd.read_csv(filepath)

            if "Ticker" not in df.columns or "Name" not in df.columns:
                raise ValueError("CSV 파일에 Ticker 또는 Name 열이 없습니다.")

            # 1) 기본 메타 저장/업서트
            tickers: list[str] = []
            for _, row in df.iterrows():
                ticker = str(row["Ticker"]).strip()
                name   = str(row["Name"]).strip()
                if not ticker or not name:
                    continue
                tickers.append(ticker)
                # merge: 존재하면 업데이트, 없으면 insert
                db.merge(Stock(ticker=ticker, name=name))
            db.commit()

            # 2) 가격/등락률 채우기 (배치로 yfinance 호출)
            self._update_prices_from_yfinance(db, tickers)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"S&P 500 저장 실패: {str(e)}"
            )

    def _update_prices_from_yfinance(self, db: Session, tickers: list[str] | None = None):
        """
        yfinance의 download를 사용해서 배치로 2일치 종가를 받는다.
        - 오늘(또는 마지막 거래일) 종가: price
        - 전일 종가와의 등락률: change_rate
        """

        if tickers is None:
            tickers = [t for (t,) in db.query(Stock.ticker).all()]
        
        # yfinance는 한 번에 너무 많이 주면 느리니 적당히 쪼갠다.
        for batch in _chunked(tickers, 50):
            try:
                # MultiIndex DF: columns = (가격필드, ticker) 또는 (ticker, 가격필드) 케이스가 있어 케이스 처리
                df = ys.download(
                    " ".join(batch),
                    period="2d",
                    interval="1d",
                    group_by="ticker",
                    auto_adjust=False,
                    progress=False,
                    threads=True,
                )

                # 티커별 두 줄(2일치) close 추출
                for t in batch:
                    close_today = None
                    close_prev  = None

                    # 케이스 1) ticker가 상위 레벨 (yfinance 버전에 따라 다름)
                    if isinstance(df.columns, pd.MultiIndex) and t in df.columns.get_level_values(0):
                        try:
                            closes = df[(t, "Close")].dropna()
                            if len(closes) >= 1:
                                close_today = float(closes.iloc[-1])
                            if len(closes) >= 2:
                                close_prev = float(closes.iloc[-2])
                        except Exception:
                            pass
                    else:
                        # 케이스 2) 단일 ticker 요청 형태처럼 반환될 수 있음
                        try:
                            closes = df["Close"].dropna()
                            if len(closes) >= 1:
                                close_today = float(closes.iloc[-1])
                            if len(closes) >= 2:
                                close_prev = float(closes.iloc[-2])
                        except Exception:
                            pass

                    price_dec = _to_decimal(close_today, "0.01")
                    change_dec = None
                    if close_today is not None and close_prev and close_prev != 0:
                        chg = ((close_today - close_prev) / close_prev) * 100.0
                        change_dec = _to_decimal(chg, "0.0001")

                    # DB 업데이트
                    stock = db.query(Stock).filter(Stock.ticker == t).first()
                    if stock:
                        stock.price = price_dec
                        stock.change_rate = change_dec

                db.commit()

            except Exception:
                db.rollback()
                # 배치 실패해도 다음 배치로 넘어가고, 실패한 배치는 무시(로그만 남기는 걸 권장)
                # logger.exception("yfinance batch update failed")
                continue
    
    def get_stock_id(self, db: db_dependency, stock_id: str) -> Stock:
        stock = db.query(Stock).filter(Stock.id == stock_id).first()
        if stock:
            return StockOut.model_validate(stock)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=("등록된 id가 없습니다")
            )
    
    def get_stock(self, db : db_dependency, search : str = "") -> List[StockOut]:
        query = db.query(Stock).order_by(Stock.ticker)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Stock.name.ilike(search_pattern),
                    Stock.ticker.ilike(search_pattern)
                )
            )

        stocks = query.all()

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
    
    def get_all_stock_interest(self, db: db_dependency, stock_id: str) -> Optional[Stock]:
        stocks = db.query(Interest).filter(Interest.stock_id == stock_id).all()

        return [InterestOut.model_validate(stock) for stock in stocks]
    
    def get_price(self, ticker: str, days: int):
        stock = ys.Ticker(ticker)
        period = f"{days}d"
        hist = stock.history(period=period)

        historical = [
            {
                "date": date.strftime("%Y-%m-%d"),
                "data": round(price, 2),
                "type": "historical"
            }
            for date, price in zip(hist.index, hist["Close"])
        ]

        return historical
    
    def get_stock_id_by_ticker(self,db:db_dependency, ticker: str) -> str | None:
        stock = db.query(Stock).filter(Stock.ticker == ticker).first()
        return str(stock.id) if stock else None
stock_service = StockService()