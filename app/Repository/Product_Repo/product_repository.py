from app.models import Product
from app.models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


def list_product_repo(user: User, db: Session):
    stmt = select(Product).where(Product.owner_id == user.id)

    result = db.execute(stmt)

    return result.scalars().all()
