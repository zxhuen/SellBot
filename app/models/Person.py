from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class Person(Base):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())