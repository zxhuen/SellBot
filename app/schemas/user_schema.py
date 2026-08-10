from unittest.mock import Base

from pydantic import BaseModel


class subscriptionType(BaseModel):
    name: str
    max_products: int
    daily_product_limit: int


class Usage(BaseModel):
    products_created_today: int


class UserResponse(BaseModel):
    email: str
    display_name: str
    avatar_url: str
    subscription: subscriptionType
    usage: Usage
