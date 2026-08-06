from sqlalchemy.orm import Session
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


def chat_services(public_id: str, message: str, response: Response, db: Session):
    session_token = ""
    if response is None:
        session_token = set_visitor_cookie(response)
    else:
        session_token = response


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
            visitor_token=visitor_token,
        )

        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)

        return chat_session

    except SQLAlchemyError:
        db.rollback()
        raise
