from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import PersonCreate, PersonResponse
from app.core.limiter import limiter
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/Login", tags=["Login"])


@router.post("/")
@limiter.limit("5/minute")
def add_person(
    request: Request,
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    return login_user(access_token, db)
