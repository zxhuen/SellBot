from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.limiter import limiter
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services.login_service.login import login_user
from app.core.security import oauth2_scheme
from app.models.User import User
from app.services.product_service.product_services import (
    create_product_with_ai,
    list_product_services,
)
from app.services.validation_service.validation import (
    get_current_user,
    check_usage_validation,
)

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
def get_product(
    access_token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list_product_services(user, db)
