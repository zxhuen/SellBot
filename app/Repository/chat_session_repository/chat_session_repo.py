from app.models.ChatSession import ChatSession
from app.models.Message import Message
from app.models.User import User
from app.models.Product import Product
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import Response


def get_chat_session_count(product_id: UUID, user_id: UUID, db: Session):
    return db.scalar(
        select(func.count(ChatSession.id))
        .join(ChatSession.product)
        .where(
            ChatSession.product_id == product_id,
            Product.owner_id == user_id,
        )
    )

def get_chat_session_by_user_and_product(
    user_id: UUID,
    product_id: UUID,
    db: Session,
) -> ChatSession | None:
    return (
        db.execute(
            select(ChatSession).where(
                ChatSession.user_id == user_id,
                ChatSession.product_id == product_id,
            )
        )
        .scalars()
        .first()
    )
