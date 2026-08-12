from uuid import UUID

from sqlalchemy.orm import Session
from app.Repository.chat_repo.chat_repository import (
    get_chat_session,
    get_messages,
    get_session_token,
)
from app.Repository.idempotency_repo.idempotency_repository import check_idempotency_key
from app.ai.content_generation.chat_generation import chat_generate
from app.ai.prompt_generator.memory_generator import generate_memory_prompt
from app.models.ChatSession import ChatSession
from app.models.Product import Product
from app.schemas import PersonCreate
from fastapi import Cookie, HTTPException, Response
import logging
from app.core.supabse_bucket import supabase
from app.models.User import User
from app.models.User_Usage import UserUsage
from app.models.Message import Message
import secrets
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.Message import Message
from app.schemas.chat_schema import ChatCreate
from app.models.IdempotencyKey import IdempotencyKey


def initialize_chat_session(
    public_id: str,
    response: Response,
    cookie: str | None,
    db: Session,
):
    if cookie is None:
        cookie = set_visitor_cookie(response)

    session_chat = get_session_token(cookie, public_id, db)

    if session_chat is None:
        session_chat = create_chat_session(
            public_id,
            cookie,
            db,
        )

        first_message = Message(
            chat_session_id=session_chat.id,
            role="assistant",
            content="Hi! Welcome! I'm Luna, and I'm here to help answer your questions and guide you through anything you need. Just send me a message to get started!",
        )

        db.add(first_message)
        db.commit()
        db.refresh(session_chat)

    chats = load_chats(session_chat.id, public_id, db)

    return chats


def set_visitor_cookie(response: Response) -> str:
    visitor_token = secrets.token_urlsafe(32)

    response.set_cookie(
        key="visitor_token",
        value=visitor_token,
        httponly=True,
        secure=True,  # MUST be True when samesite="none"
        samesite="none",  # Required for cross-site POST requests
        max_age=60 * 60 * 24 * 365,
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


def load_chats(chat_session_id: UUID, public_id: str, db: Session):
    return get_messages(chat_session_id, public_id, db)


async def send_chat(chat: ChatCreate, public_id: str, cookie: str, db: Session):
    chat_session = get_chat_session(cookie, public_id, db)

    if chat_session is None:
        raise HTTPException(status_code=404, detail="No chat session found")

    try:
        # check idempotency key
        idempotency_key = check_idempotency_key(chat.idempotecy_key, chat_session.id)

        if idempotency_key:
            return idempotency_key.response

        message_history = get_messages(chat_session.id, public_id, db)

        llm_messages = [
            {"role": message.role, "content": message.content}
            for message in message_history
        ]

        user_message = Message(
            chat_session_id=chat_session.id, role="User", content=chat.message
        )
        db.add(user_message)

        generated_prompt = generate_memory_prompt(
            chat_session.product, llm_messages, chat.message
        )

        response = await chat_generate(generated_prompt)

        llm_message = Message(
            chat_session_id=chat_session.id, role="Assistant", content=response
        )
        db.add(llm_message)

        key = IdempotencyKey(
            key=chat.idempotecy_key, chat_session_id=chat_session.id, response=response
        )
        db.add(key)

        db.commit()

        return response

    except Exception:
        db.rollback()
        raise
