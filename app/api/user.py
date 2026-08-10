from fastapi import APIRouter, Request, Depends
from app.core.limiter import limiter
from app.models.User import User
from app.services.validation_service.validation import (
    get_current_user,
)

router = APIRouter(prefix="/User", tags=["User"])


@router.post("/show-profile")
@limiter.limit("30/minute")
async def show_profile(
    request: Request,
    user: User = Depends(get_current_user),
):
    return user
