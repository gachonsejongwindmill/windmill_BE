import os
from dotenv import load_dotenv

import requests
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from api.utils.dependency import get_db

load_dotenv()

NAVER_CLIENT_ID=os.environ.get("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET=os.environ.get("NAVER_CLIENT_SECRET")
NAVER_NEWS_URL= "https://openapi.naver.com/v1/search/news.json"
db_dependency = Annotated(Session,Depends(get_db))

class NewsService:
    def get_headers(self):
        return {
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        }
    def get_news(self, query: str = "경제 OR 금융 OR S&P500", display: int = 10, start: int = 1, sort: str = "date"):
        headers = self.get_headers()
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }

        response = requests.get(NAVER_NEWS_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()

        return [
            {
                "title": item["title"],
                "link": item["link"],
                "description": item["description"],
                "pubDate": item["pubDate"]
            }
            for item in data.get("items", [])
        ]
    
news_service = NewsService()