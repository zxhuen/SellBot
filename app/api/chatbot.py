from fastapi import APIRouter, Request, Depends, Response, Cookie
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.chat_schema import ChatCreate
from app.services.chat_service.chat_services import initialize_chat_session, send_chat
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme
from app.services.validation_service.validation import get_current_user
from app.models.User import User

router = APIRouter(prefix="/Chat", tags=["Chat"])


@router.post("/Luna")
@limiter.limit("50/day")
async def chat_luna(
    request: Request,
    chat: ChatCreate,
    public_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await send_chat(
        chat,
        public_id,
        current_user,
        db,
    )


@router.get("/Load-Chat")
@limiter.limit("10/minute")
def load_chat(
    request: Request,
    public_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return initialize_chat_session(public_id, current_user, db)
