from uuid import UUID

from sqlalchemy.orm import Session

from app.Repository.Product_Repo.buy_repository import get_user_chat_sessions
from app.models.ChatSession import ChatSession


def get_chat_sessions(
    db: Session,
    user_id: UUID,
) -> list[ChatSession]:
    return get_user_chat_sessions(db, user_id)



