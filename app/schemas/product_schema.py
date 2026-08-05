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
    price: Decimal

    class Config:
        from_attributes = True
