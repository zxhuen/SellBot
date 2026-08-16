from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import UniqueConstraint

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

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )

    session_token: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

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

    product: Mapped["Product"] = relationship(back_populates="chat_sessions")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "session_token",
            name="uq_chat_session_product_token",
        ),
    )
