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

app = FastAPI()

app.include_router(route)

# 프론트와 연결을 위해
origins = ["https://windmill-w219-gttashl9d-iborys-projects.vercel.app/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://windmill-w219-gttashl9d-iborys-projects.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return success_response(message = "welcome")