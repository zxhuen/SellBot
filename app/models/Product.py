from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UUID,
    func,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.ChatSession import ChatSession


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: uuid4(),
    )

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    public_id: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, index=true
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="available",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(back_populates="products")
    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )
