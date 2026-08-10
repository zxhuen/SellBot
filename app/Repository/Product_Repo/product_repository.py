from requests import session

from app.models import Product
from app.models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from app.models.ChatSession import ChatSession
from app.models.Message import Message


def list_product_repo(user: User, db: Session):
    stmt = select(Product).where(Product.owner_id == user.id)

    result = db.execute(stmt)

    return result.scalars().all()


def get_product(user: User, id: UUID, db: Session):
    stmt = select(Product).where(
        Product.owner_id == user.id,
        Product.id == id,
    )

    result = db.execute(stmt)

    return result.scalars().first()


def get_product_public_id(public_id: UUID, db: Session):
    stmt = select(Product).where(
        Product.public_id == public_id,
    )

    result = db.execute(stmt)

    return result.scalars().first()


def mark_product_as_sold(id: UUID, user: User, db: Session):
    stmt = select(Product).where(Product.id == id, Product.owner_id == user.id)

    result = db.execute(stmt)

    return result.scalars().first()
