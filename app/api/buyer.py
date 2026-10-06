from fastapi import APIRouter, Depends
from fastapi import Request
from pytest import Session
from supabase_auth import User
from app.core.database import get_db
from app.core.limiter import limiter
from app.services.product_service.buy_services import get_chat_sessions
from app.services.validation_service.validation import get_current_user

router = APIRouter(prefix="/Buyer", tags=["Buyer"])


@router.get("/List-Chat-Sessions")
async def list_chat_sessions(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_chat_sessions(db, user.id)
