from app.models.ChatSession import ChatSession
from app.models.Message import Message
from app.models.User import User
from app.models.Product import Product
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import Response


def get_session_token(cookie: str, public_id: str, db: Session):
    stmt = (
        select(ChatSession)
        .options(joinedload(ChatSession.product))
        .join(ChatSession.product)
        .where(
            ChatSession.session_token == cookie,
            Product.public_id == public_id,
        )
    )

    result = db.execute(stmt)

    return result.scalars().first()


def get_messages(session_id: UUID, public_id: str, db: Session):
    stmt = (
        select(Message)
        .where(Message.chat_session_id == session_id)
        .order_by(Message.created_at.asc())
    )

    result = db.execute(stmt)

    return result.scalars().all()


def get_chat_session(cookie: str, public_id: str, db: Session):
    print("COOKIE:", repr(cookie))

    stmt = (
        select(ChatSession)
        .options(joinedload(ChatSession.product))
        .join(ChatSession.product)
        .where(
            ChatSession.session_token == cookie,
            Product.public_id == public_id,
        )
    )

    result = db.execute(stmt)

    chat_session = result.scalars().first()

    print("CHAT SESSION:", chat_session)

    return chat_session
