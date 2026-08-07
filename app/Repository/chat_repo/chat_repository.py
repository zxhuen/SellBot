from app.models import ChatSession, Message
from app.models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import Response


def get_session_token(cookie: str, db: Session):
    stmt = select(ChatSession).where(
        ChatSession.session_token == cookie,
    )

    result = db.execute(stmt)

    return result.scalars().first()


def get_messages(session_id: UUID, db: Session):
    stmt = (
        select(Message)
        .where(Message.chat_session_id == session_id)
        .order_by(Message.created_at.asc())
    )

    result = db.execute(stmt)

    return result.scalars().all()
