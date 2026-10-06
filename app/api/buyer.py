from fastapi import APIRouter
from fastapi import Request
from app.core.limiter import limiter
from app.services.product_service.buy_services import get_chat_sessions

router = APIRouter(prefix="/Buyer", tags=["Buyer"])


@router.get("List-Chat-Sessions")
async def list_chat_sessions(request: Request):
    return get_chat_sessions()
