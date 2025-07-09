from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.utils.database import Base, engine
from api.routers import route
from api.models import *

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(route)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)