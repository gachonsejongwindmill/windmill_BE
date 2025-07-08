from fastapi import APIRouter
from api.routers.auth import auth
route = APIRouter()

route.include_router(auth)