from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class ProductCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str = Field(
        min_length=1,
        max_length=1000,
    )

    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    contact_link: HttpUrl


class ProductResponse(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal
    public_id: str
    status: str

    class Config:
        from_attributes = True


class PublicProductResponse(BaseModel):
    title: str
    description: str
    price: Decimal
    contact_link: HttpUrl

    class Config:
        from_attributes = True

class ChatSessionProductResponse(BaseModel):
    title: str
    price: Decimal

    class Config:
        from_attributes = True

class ChatSessionUserResponse(BaseModel):
    display_name: str
    avatar_url: str | None = None

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    product: ChatSessionProductResponse
    user: ChatSessionUserResponse
    last_message_at: datetime

    class Config:
        from_attributes = True


