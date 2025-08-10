# api/services/indicator.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Iterable, Optional, Dict, Any, List, Annotated

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
        yfinance로 최근 2영업일 종가를 가져와 current/등락률(%) 갱신.
        futures/지수/환율 티커도 그대로 yfinance가 처리.
        """
        if tickers is None:
            tickers = [t[0] for t in db.query(Indicator.ticker).all()]
        tickers_list: List[str] = list(dict.fromkeys(tickers))  # 중복 제거/순서 유지

        updated = 0
        skipped: List[str] = []

        for i in range(0, len(tickers_list), batch_size):
            chunk = tickers_list[i:i+batch_size]
            if not chunk:
                continue

            data = yf.download(
                " ".join(chunk),
                period=period,
                interval=interval,
                group_by="ticker",
                auto_adjust=False,
                threads=True,
                progress=False,
            )

            for t in chunk:
                try:
                    # 단일 티커일 때는 컬럼 구조가 달라져서 분기
                    if len(chunk) == 1:
                        closes = data["Close"].dropna().tail(2)
                    else:
                        closes = data[t]["Close"].dropna().tail(2)

                    if len(closes) < 2:
                        skipped.append(t)
                        continue

                    prev_close = float(closes.iloc[-2])
                    last_close = float(closes.iloc[-1])
                    change_pct = ((last_close - prev_close) / prev_close * 100.0) if prev_close else 0.0

                    db.execute(
                        update(Indicator)
                        .where(Indicator.ticker == t)
                        .values(
                            current=round(last_close, 4),
                            change_rate=round(change_pct, 4),
                            price_updated_at=datetime.now(timezone.utc),
                        )
                    )
                    updated += 1
                except Exception:
                    skipped.append(t)
                    continue

        db.commit()
        return {"updated": updated, "skipped": skipped}
    
    def get_indicator(self, db: db_dependency):
        indicators = db.query(Indicator).all()
        return [IndicatorOut.model_validate(indicator) for indicator in indicators]

indicator_service = IndicatorService()
