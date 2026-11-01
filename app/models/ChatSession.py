from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import Index, UniqueConstraint

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UUID,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.Message import Message


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=False,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    last_message_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="chat_sessions",
    )

    product: Mapped["Product"] = relationship(
        back_populates="chat_sessions",
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    __table_args__ = (
     UniqueConstraint(
        "user_id",
        "product_id",
        name="uq_chat_session_user_product",
     ),
     Index(
        "ix_chat_sessions_user_last_message",
        "user_id",
        last_message_at.desc(),
        id
     ),
    )   

    
