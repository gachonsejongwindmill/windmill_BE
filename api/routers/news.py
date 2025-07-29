from fastapi import APIRouter, Query

from api.services.news import news_service
from api.responses.success_response import success_response

news = APIRouter(prefix="/news", tags=['news'])

@news.get("")
def fetch_news(
    query: str = Query("경제 OR 금융 OR S&P500", description="검색 키워드"),
    display: int = Query(10, ge=1, le=100, description="가져올 뉴스 수 (최대 100)"),
    start: int = Query(1, ge=1, description="시작 위치"),
    sort: str = Query("date", pattern="^(date|sim)$", description="정렬 기준 (date | sim)")
):
    data = news_service.get_news(query=query, display=display, start=start, sort=sort)
    return success_response(
        message=f"{query}에 관련된 {display}개의 기사를 {sort}로 정렬시켜 {start}번째부터 출력합니다",
        data=data
    )