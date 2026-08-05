from app.models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.User import User


def list_product_repo(user: User, db: Session):
    stmt = select(User).options(joinedload(User.products)).where(User.id == user.id)

    result = db.execute(stmt)
    return result.unique().scalar_one()
