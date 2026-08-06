from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str
    price: Decimal


class ProductResponse(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal
    public_id: str

    class Config:
        from_attributes = True


class PublicProductResponse(BaseModel):
    title: str
    description: str
    price: Decimal

    class Config:
        from_attributes = True
