from fastapi import APIRouter
from api.routers.auth import auth
from api.routers.user import user
from api.routers.stock import stock
from api.routers.predict import predict
from api.routers.news import news

route = APIRouter()

route.include_router(auth)
route.include_router(user)
route.include_router(stock)
route.include_router(predict)
route.include_router(news)