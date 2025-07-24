from fastapi import APIRouter
from api.routers.auth import auth
from api.routers.user import user
from api.routers.stock import stock
from api.routers.predict import predict

route = APIRouter()

route.include_router(auth)
route.include_router(user)
route.include_router(stock)