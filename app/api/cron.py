from fastapi import APIRouter
from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(prefix="/Cron", tags=["Cron"])


@router.post("/Cron")
@limiter.limit("3/minute")
async def cron_request(request: Request):
    return "Hello World"
