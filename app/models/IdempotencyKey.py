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
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = mapped_column(UUID, primary_key=True, default=uuid4)
    key = mapped_column(String, unique=True, nullable=False)
    chat_session_id = mapped_column(
        UUID,
        ForeignKey("chat_sessions.id"),
        nullable=False,
    )
    response = mapped_column(Text, nullable=True)
    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
