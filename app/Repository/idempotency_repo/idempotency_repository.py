from app.models.ChatSession import ChatSession
from app.models.Message import Message
from app.models.User import User
from app.models.Product import Product
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import Response
from app.models.IdempotencyKey import IdempotencyKey


def check_idempotency_key(idempotency_key: UUID, chat_session_id: UUID, db: Session):
    return (
        db.query(IdempotencyKey)
        .filter(
            IdempotencyKey.key == idempotency_key,
            IdempotencyKey.chat_session_id == chat_session_id,
        )
        .first()
    )
