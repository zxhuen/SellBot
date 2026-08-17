from email import message
from math import prod
from uuid import uuid4
from sqlalchemy.orm import Session
from app.Repository.Product_Repo.product_repository import (
    get_product,
    get_product_public_id,
    list_product_repo,
    mark_product_as_sold,
)
from app.Repository.chat_session_repository.chat_session_repo import (
    get_chat_session_count,
)
from app.ai.content_generation.product_description_generation import (
    product_description_gemini_response,
)
from app.ai.prompt_generator.product_description_generator import (
    generate_product_desc_prompt,
)
from app.models.Product import Product
from app.schemas import PersonCreate
from fastapi import HTTPException
import logging
from app.core.supabse_bucket import supabase
from app.models.User import User
from app.models.User_Usage import UserUsage
from app.schemas.product_schema import ProductCreate
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.models.User_Usage import UserUsage


def load_analytics(product_id: UUID, user: User, db: Session):
    chat_session_count = get_chat_session_count(product_id, user.id, db)

    return {"visitors_who_messaged": chat_session_count}
