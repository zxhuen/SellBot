from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import PersonCreate, PersonResponse
from app.core.limiter import limiter

router = APIRouter(prefix="/Login", tags=["Login"])
