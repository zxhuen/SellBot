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
from app.schemas.product_schema import ProductCreate, ProductResponse
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from app.models.User_Usage import UserUsage
from app.core.redis import redis_client
import json


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

        with db.begin():
            usage = (
                db.query(UserUsage)
                .filter(UserUsage.user_id == user.id)
                .with_for_update()
                .one()
            )

            if usage.products_created_today >= user.subscription.daily_product_limit:
                raise HTTPException(
                    status_code=403,
                    detail="You have reached your daily product creation limit.",
                )

            db.add(new_product)
            usage.products_created_today += 1

        db.refresh(new_product)

        cache_key = f"user_id:{user.id}"

        redis_client.delete(cache_key)

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
    cache_key = f"user_id:{user.id}"
    cached_user = redis_client.get(cache_key)

    if cached_user:
        return json.loads(cached_user)

    products = list_product_repo(user, db)

    if products is None:
        raise HTTPException(status_code=404, detail="no products found")

    response = [
        ProductResponse.model_validate(product).model_dump(mode="json")
        for product in products
    ]

    redis_client.set(cache_key, json.dumps(response), ex=60 * 60)

    return products


def delete_product_service(id: UUID, user: User, db: Session):

    products = get_product(user, id, db)

    if products is None:
        raise HTTPException(status_code=404, detail="no products found")

    db.delete(products)
    db.commit()

    cache_key = f"user_id:{user.id}"

    redis_client.delete(cache_key)

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
