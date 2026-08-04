from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/Validate", tags=["Validate"])


@router.post("/")
@limiter.limit("10/minute")
def validate_current_user(
    request: Request,
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    print("HelloWorld")
