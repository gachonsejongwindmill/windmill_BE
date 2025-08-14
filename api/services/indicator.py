# api/services/indicator.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Iterable, Optional, Dict, Any, List, Annotated
import pandas as pd
import yfinance as yf
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update

from api.models.indicator import Indicator
from api.utils.dependency import get_db
from api.schemas.indicator import IndicatorOut


db_dependency = Annotated[Session,Depends(get_db)]

INDICATOR_SEED = [
    {"name": "S&P 500",               "ticker": "^GSPC"},
    {"name": "Dow Jones (다우존스)",   "ticker": "^DJI"},
    {"name": "NASDAQ Composite",      "ticker": "^IXIC"},
    {"name": "VIX",                   "ticker": "^VIX"},
    {"name": "MSCI World (URTH ETF)", "ticker": "URTH"},
    {"name": "KOSPI",                 "ticker": "^KS11"},
    {"name": "KOSDAQ",                "ticker": "^KQ11"},
    {"name": "USD/KRW",               "ticker": "KRW=X"},
    {"name": "WTI 유가",               "ticker": "CL=F"},
    {"name": "Gold 선물",               "ticker": "GC=F"},
]
# 가격이 아직 안불러와짐
class IndicatorService:
    def seed_indicators(self, db: db_dependency) -> Dict[str, int]:
        inserted = 0
        for row in INDICATOR_SEED:
            exists = db.query(Indicator).filter(Indicator.ticker == row["ticker"]).first()
            if not exists:
                db.add(Indicator(name=row["name"], ticker=row["ticker"]))
                inserted += 1
        db.commit()
        return {"inserted": inserted, "total": db.query(Indicator).count()}

   
    def update_prices(
        self,
        db: db_dependency,
        tickers: Optional[Iterable[str]] = None,
        period: str = "7d",
        interval: str = "1d",
        batch_size: int = 20,
    ) -> Dict[str, Any]:
        """
        yfinance로 최근 2개 종가를 가져와 current / change_rate(%) 갱신.
        """
        # 0) 대상 티커 수집
        if tickers is None:
            tickers = [t for (t,) in db.query(Indicator.ticker).all()]
        tickers_list: List[str] = list(dict.fromkeys([t.strip() for t in tickers if t and t.strip()]))

        updated = 0
        skipped: List[str] = []
        skipped_detail: Dict[str, str] = {}

        def _extract_close_series(df: pd.DataFrame, symbol: str) -> pd.Series:
            """
            yfinance가 반환하는 DataFrame에서 특정 symbol의 Close 시리즈를 빼온다.
            - 단일 심볼: columns가 단순 Index -> df['Close']
            - 다중 심볼: columns가 MultiIndex -> df['Close'][symbol]
            """
            if df.empty:
                raise ValueError("empty dataframe")

            if isinstance(df.columns, pd.MultiIndex):
                # 예: columns level0: ['Adj Close','Close',...] / level1: [AAPL, MSFT, ...]
                if 'Close' not in df.columns.get_level_values(0):
                    raise KeyError("Close column not found (multiindex)")
                if symbol not in df['Close'].columns:
                    raise KeyError(f"symbol {symbol} not in Close columns")
                s = df['Close'][symbol].dropna()
            else:
                # 단일 티커일 때는 Close 컬럼이 바로 존재해야 함
                if 'Close' not in df.columns:
                    raise KeyError("Close column not found (single)")
                s = df['Close'].dropna()
            return s

        # 1) 배치로 다운로드
        for i in range(0, len(tickers_list), batch_size):
            chunk = tickers_list[i:i + batch_size]
            if not chunk:
                continue

            try:
                # 리스트 그대로 넘긴다(공백 연결 X) → 특수문자 티커 안전
                data = yf.download(
                    tickers=chunk,
                    period=period,
                    interval=interval,
                    group_by="ticker",  # 멀티티커면 MultiIndex, 단일 티커면 일반 컬럼
                    auto_adjust=False,
                    threads=True,
                    progress=False,
                )
            except Exception as e:
                # 이 덩어리 통째로 실패하면 전부 skip
                for t in chunk:
                    skipped.append(t)
                    skipped_detail[t] = f"download error: {repr(e)}"
                continue

            # 2) 각 티커별로 close 2개 뽑아서 계산/업데이트
            for t in chunk:
                try:
                    closes = _extract_close_series(data, t).tail(2)
                    if len(closes) < 2:
                        skipped.append(t)
                        skipped_detail[t] = "not enough candles (<2)"
                        continue

                    prev_close = float(closes.iloc[-2])
                    last_close = float(closes.iloc[-1])
                    change_pct = ((last_close - prev_close) / prev_close * 100.0) if prev_close else 0.0

                    stmt = (
                        update(Indicator)
                        .where(Indicator.ticker == t)
                        .values(
                            current=round(last_close, 4),
                            change_rate=round(change_pct, 4),
                            price_updated_at=datetime.now(timezone.utc),
                        )
                    )
                    db.execute(stmt)
                    updated += 1

                except Exception as e:
                    skipped.append(t)
                    skipped_detail[t] = repr(e)
                    continue

        db.commit()
        return {"updated": updated, "skipped": skipped, "skipped_detail": skipped_detail}

    
    def get_indicator(self, db: db_dependency):
        indicators = db.query(Indicator).all()
        return [IndicatorOut.model_validate(indicator) for indicator in indicators]

indicator_service = IndicatorService()
