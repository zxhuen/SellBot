from email import message
from math import prod
from uuid import uuid4
from sqlalchemy.orm import Session
from app.Repository.Product_Repo.product_repository import (
    get_product,
    get_product_public_id,
    list_product_repo,
    list_seller_product_messages,
    mark_product_as_sold,
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


def create_product(product: ProductCreate, user: User, db: Session):
    try:
        new_product = Product(
            id=uuid4(),
            owner_id=user.id,
            title=product.title,
            description=product.description,
            price=product.price,
            public_id=uuid4().hex[:12],
        )

        db.add(new_product)
        user.usage.products_created_today += 1

        db.commit()
        db.refresh(new_product)

        return new_product

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create product.",
        ) from e


async def revise_description(description: str):
    revised_description = generate_product_desc_prompt(description)
    response = await product_description_gemini_response(revised_description)
    return response


async def create_product_with_ai(product: ProductCreate, user: User, db: Session):
    improvised_description = await revise_description(product.description)
    product.description = improvised_description
    return create_product(product, user, db)


def list_product_services(user: User, db: Session):
    products = list_product_repo(user, db)

    if products is None:
        raise HTTPException(status_code=404, detail="no products found")

    return products


def delete_product_service(id: UUID, user: User, db: Session):
    products = get_product(user, id, db)

    if products is None:
        raise HTTPException(status_code=404, detail="no products found")

    db.delete(products)
    db.commit()

    return {"message": "Product deleted successfully"}


def get_product_throught_public_id(public_id: str, db: Session):
    product = get_product_public_id(public_id, db)

    if product is None:
        raise HTTPException(status_code=404, detail="no products found")

    return product


def mark_as_sold_service(id: UUID, user: User, db: Session):
    product = mark_product_as_sold(id, user, db)

    if product.status == "Sold":
        raise HTTPException(status_code=404, detail="Product is already sold")

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product.status = "Sold"
    db.commit()
    db.refresh(product)

    return {"mesage": "product is already set as sold"}

def list_messages(user_id: UUID, product_id: UUID, db: Session):
    messages = list_seller_product_messages()
