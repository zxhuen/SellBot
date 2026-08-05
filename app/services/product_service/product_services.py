from uuid import uuid4
from sqlalchemy.orm import Session
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


def create_product(product: ProductCreate, user: User, db: Session):
    new_product = Product(
        id=uuid4(),
        owner_id=user.id,
        title=product.title,
        description=product.description,
        price=product.price,
        public_id=str(uuid4().hex[:12]),  # or however you generate your public IDs
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


async def revise_description(description: str):
    revised_description = generate_product_desc_prompt(description)
    response = await product_description_gemini_response(revised_description)
    return response


async def create_product_with_ai(product: ProductCreate, user: User, db: Session):
    improvised_description = await revise_description(product.description)
    product.description = improvised_description
    return create_product(product, user, db)
