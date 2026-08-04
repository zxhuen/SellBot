from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserUsage(Base):
    __tablename__ = "user_usages"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    products_created_today: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    last_reset_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="usage",
    )
