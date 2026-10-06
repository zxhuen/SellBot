from requests import session

from app.models import Product
from app.models.User import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from app.models.ChatSession import ChatSession
from app.models.Message import Message


def get_user_chat_sessions(
    db: Session,
    user_id: UUID,
) -> list[ChatSession]:

    stmt = (
        select(ChatSession)
        .options(joinedload(ChatSession.product))
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.last_message_at.desc())
    )

    result = db.execute(stmt)

    return result.scalars().all()


