from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True
