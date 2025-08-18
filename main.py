import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.utils.database import Base, engine
from api.routers import route
from api.models import *
from api.responses.success_response import success_response

app = FastAPI(redirect_slashes=False)

app.include_router(route)

# 프론트와 연결을 위해
origins = [
    "http://localhost:3000",   # 개발용
    "https://windmill-w219.vercel.app",  # 배포된 프론트엔드
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return success_response(message = "welcome")