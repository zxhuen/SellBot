from uuid import UUID

from sqlalchemy.orm import Session
from app.Repository.chat_repo.chat_repository import (
    get_chat_session,
    get_messages,
    get_session_token,
)
from app.Repository.chat_session_repository.chat_session_repo import get_chat_session_by_user_and_product
from app.Repository.idempotency_repo.idempotency_repository import check_idempotency_key
from app.ai.content_generation.chat_generation import chat_generate
from app.ai.prompt_generator.memory_generator import generate_memory_prompt
from app.models.ChatSession import ChatSession
from app.models.Product import Product
from app.schemas import PersonCreate
from fastapi import Cookie, HTTPException, Response, logger
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
from app.core.redis import redis_client
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone
from redis.exceptions import LockError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

def initialize_chat_session(
    public_id: str,
    current_user: User,
    db: Session,
):
    session_chat = get_chat_session(
        public_id,
        current_user.id,
        db,
    )

    if session_chat is None:
        session_chat = create_chat_session(
            public_id,
            current_user.id,
            db,
        )

    return load_chats(
        session_chat.id,
        db,
    )





def create_chat_session(
    public_id: str,
    user_id: UUID,
    db: Session,
):
    lock = redis_client.lock(
        f"chat_session:{user_id}:{public_id}",
        timeout=30,
        blocking_timeout=10,
    )

    if not lock.acquire():
        raise HTTPException(
            status_code=409,
            detail="Another session creation is already in progress",
        )

    product = None

    try:
        with db.begin():
            product = (
                db.execute(
                    select(Product).where(
                        Product.public_id == public_id
                    )
                )
                .scalars()
                .first()
            )

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found",
                )

            existing_session = get_chat_session_by_user_and_product(
                user_id,
                product.id,
                db,
            )

            if existing_session is not None:
                return existing_session

            chat_session = ChatSession(
                user_id=user_id,
                product_id=product.id,
            )

            db.add(chat_session)
            db.flush()

            first_message = Message(
                chat_session_id=chat_session.id,
                role="assistant",
                content=(
                    "Hi! Welcome! I'm Luna, and I'm here to help answer "
                    "your questions and guide you through anything you need. "
                    "Just send me a message to get started!"
                ),
            )

            db.add(first_message)
            db.flush()

        db.refresh(chat_session)

        return chat_session

    except IntegrityError:
        if product is not None:
            existing_session = get_chat_session_by_user_and_product(
                user_id,
                product.id,
                db,
            )

            if existing_session is not None:
                return existing_session

        raise

    finally:
        try:
            lock.release()
        except LockError:
            logger.warning(
                "Chat session lock expired or was no longer owned: %s",
                lock.name,
            )


def load_chats(
    chat_session_id: UUID,
    db: Session,
):
    return get_messages(
        chat_session_id,
        db,
    )



async def send_chat(
    chat: ChatCreate,
    public_id: str,
    current_user: User,
    db: Session,
):
    # 1. Retrieve chat session and verify ownership
    chat_session = get_chat_session(
        public_id,
        current_user.id,
        db,
    )

    if chat_session is None:
        raise HTTPException(
            status_code=404,
            detail="No chat session found",
        )

    # 2. Capture conversation version
    expected_version = chat_session.version

    # 3. Retrieve conversation history
    message_history = get_messages(
        chat_session.id,
        db,
    )

    llm_messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in message_history
    ]

    # 4. Generate LLM response outside transaction
    generated_prompt = generate_memory_prompt(
        chat_session.product,
        llm_messages,
        chat.message,
    )

    response = await chat_generate(generated_prompt)

    # 5. Atomically validate version and persist messages
    try:
        with db.begin():

            result = db.execute(
                update(ChatSession)
                .where(
                    ChatSession.id == chat_session.id,
                    ChatSession.version == expected_version,
                )
                .values(
                    version=ChatSession.version + 1,
                    last_message_at=datetime.now(timezone.utc),
                )
            )

            # 6. Reject conflicting requests
            if result.rowcount != 1:
                raise HTTPException(
                    status_code=409,
                    detail="Conversation changed. Please retry.",
                )

            # 7. Persist user message
            user_message = Message(
                chat_session_id=chat_session.id,
                role="User",
                content=chat.message,
            )

            db.add(user_message)

            # 8. Persist assistant response
            llm_message = Message(
                chat_session_id=chat_session.id,
                role="Assistant",
                content=response,
            )

            db.add(llm_message)

        # Transaction automatically commits here

        return response

    except Exception:
        db.rollback()
        raise
