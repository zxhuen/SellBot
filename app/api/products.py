from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.Repository.Product_Repo.product_repository import get_product_chat_session
from app.core.database import async_get_db, get_db
from app.core.limiter import limiter
from app.schemas.chat_schema import MessageResponse
from app.schemas.product_schema import (
    ChatSessionProductResponse,
    ChatSessionResponse,
    ProductCreate,
    ProductResponse,
    PublicProductResponse,
)
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme
from app.models.User import User
from uuid import UUID
from app.services.product_service.product_services import (
    create_product_with_ai,
    delete_product_service,
    get_product_chat_session_service,
    get_product_throught_public_id,
    list_product_services,
    load_chat_messages,
    mark_as_sold_service,
)
from app.services.validation_service.validation import (
    get_current_user,
    check_usage_validation,
)

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/Products", tags=["Products"])


@router.post("/add-product", response_model=ProductResponse)
@limiter.limit("4/minute")
async def add_product(
    request: Request,
    product: ProductCreate,
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    check_usage_validation(user, db)

    return await create_product_with_ai(product, user, db)


@router.get("/list-product", response_model=list[ProductResponse])
@limiter.limit("20/minute")
def get_product(
    request: Request,
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list_product_services(user, db)


@router.delete("/delete-product")
def delete_product(
    id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return delete_product_service(id, user, db)


@router.get("/get-product-public-id", response_model=PublicProductResponse)
@limiter.limit("5/minute")
def get_product_public_id(
    request: Request, public_id: str, db: Session = Depends(get_db)
):
    return get_product_throught_public_id(public_id, db)


@router.patch("/mark-as-sold")
@limiter.limit("5/minute")
def mark_as_sold(
    request: Request,
    id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return mark_as_sold_service(id, user, db)


@router.get("/get-product-history", response_model=list[ChatSessionResponse])
@limiter.limit("6/minute")
def get_product_history(
    request: Request,
    product_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_product_chat_session_service(product_id, user, db)

@router.get("/get-chat-messages", response_model=list[MessageResponse])
@limiter.limit("10/minute")
async def fetch_chat_messages(
    request: Request,
    chat_session_id: UUID,
    db: AsyncSession = Depends(async_get_db),
    current_user: User = Depends(get_current_user),
):
    return await load_chat_messages(
        db=db,
        chat_session_id=chat_session_id,
        user_id=current_user.id,
    )