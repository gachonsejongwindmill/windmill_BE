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
db_dependency = Annotated(Session,Depends(get_db))