from fastapi import APIRouter
from api.routers.auth import auth
from api.routers.user import user

route = APIRouter()

route.include_router(auth)
route.include_router(user)