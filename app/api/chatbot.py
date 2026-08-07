from fastapi import APIRouter, Request, Depends, Response, Cookie
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.chat_schema import ChatCreate
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/Chat", tags=["Chat"])


@router.post("/Luna")
@limiter.limit("10/minute")
def chat_luna(
    request: Request,
    chat: ChatCreate,
    response: Response,
    session_token: str | None = Cookie(default=None)
    db: Session = Depends(get_db),
):
    
