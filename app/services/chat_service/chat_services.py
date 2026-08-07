from uuid import UUID

from sqlalchemy.orm import Session
from app.Repository.chat_repo.chat_repository import get_messages, get_session_token
from app.models import ChatSession
from app.models.Product import Product
from app.schemas import PersonCreate
from fastapi import HTTPException, Response
import logging
from app.core.supabse_bucket import supabase
from app.models.User import User
from app.models.User_Usage import UserUsage
import secrets
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.Message import Message


def initialize_chat_session(
    public_id: str, response: Response, cookie: str, db: Session
):
    if cookie is None:
        session_token = set_visitor_cookie(response)

        chat_session = create_chat_session(public_id, session_token, db)
        first_message = Message(
            chat_session_id=chat_session.id,
            role="assistant",
            content="Hi! Welcome! I'm Luna, and I'm here to help answer your questions and guide you through anything you need. Just send me a message to get started!",
        )

        db.add(first_message)
        db.commit()
        db.refresh(first_message)

    session_chat = get_session_token(cookie, db)

    if session_chat is None:
        raise HTTPException(status_code=404, message="no chat session found")

    chats = load_chats(session_chat.id)

    return chats


def set_visitor_cookie(response: Response) -> str:
    visitor_token = secrets.token_urlsafe(32)

    response.set_cookie(
        key="visitor_token",
        value=visitor_token,
        httponly=True,
        secure=False,  # False during local development if not using HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 365,  # 1 year
    )

    return visitor_token


def create_chat_session(public_id: str, visitor_token: str, db: Session):
    product = (
        db.execute(select(Product).where(Product.public_id == public_id))
        .scalars()
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        chat_session = ChatSession(
            product_id=product.id,
            session_token=visitor_token,
        )

        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

        return chat_session

    except SQLAlchemyError:
        db.rollback()
        raise


def load_chats(chat_session_id: UUID, db: Session):
    return get_messages(chat_session_id, db)
