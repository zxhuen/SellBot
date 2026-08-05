from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, Depends
from app.Repository.Product_Repo.product_repository import list_product_repo
from app.core.supabse_bucket import supabase
from app.models import User, UserUsage
from app.core.security import oauth2_scheme
from app.core.database import get_db
from datetime import UTC, datetime, timedelta
from app.models.Product import Product


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        response = supabase.auth.get_user(token)
        auth_user = response.user

        if auth_user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token.",
            )

        user = (
            db.query(User)
            .filter(User.id == auth_user.id)
            .options(joinedload(User.subscription), joinedload(User.usage))
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found.",
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )


def check_usage_validation(user: User, db: Session):
    usage = user.usage
    subscription = user.subscription

    # Reset daily usage every 24 hours
    if datetime.now(UTC) - usage.last_reset_at >= timedelta(hours=24):
        usage.products_created_today = 0
        usage.last_reset_at = datetime.now(UTC)
        db.commit()

    # Daily product creation limit
    if usage.products_created_today >= subscription.daily_product_limit:
        raise HTTPException(
            status_code=403,
            detail="You have reached your daily product creation limit.",
        )

    # Total product limit
    total_products = list_product_repo(user, db)

    if len(total_products) >= subscription.max_products:
        raise HTTPException(
            status_code=403,
            detail="You have reached the maximum number of products for your subscription.",
        )
