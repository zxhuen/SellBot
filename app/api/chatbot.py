from fastapi import APIRouter, Request, Depends, Response, Cookie
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.chat_schema import ChatCreate
from app.services.chat_service.chat_services import initialize_chat_session, send_chat
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/Chat", tags=["Chat"])


@router.post("/Luna")
@limiter.limit("10/minute")
async def chat_luna(
    request: Request,
    chat: ChatCreate,
    visitor_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    return await send_chat(chat, visitor_token, db)


@router.get("/Load-Chat")
@limiter.limit("5/minute")
def load_chat(
    request: Request,
    response: Response,
    public_id: str,
    visitor_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    return initialize_chat_session(public_id, response, visitor_token, db)
