from fastapi import APIRouter, Request, Depends, Response, Cookie
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from app.models.User import User
from app.schemas.chat_schema import ChatCreate
from app.services.analytics_service.analytics_services import load_analytics
from app.services.chat_service.chat_services import initialize_chat_session, send_chat
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme
from app.services.validation_service.validation import get_current_user
from uuid import UUID

router = APIRouter(prefix="/Analytics", tags=["Analytics"])


@router.post("/get-chat-session-count")
@limiter.limit("10/minute")
async def chat_luna(
    request: Request,
    product_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return load_analytics(product_id, current_user, db)
