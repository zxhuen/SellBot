from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ChatCreate(BaseModel):
    message: str = Field(max_length=500)
    ##idempotecy_key: str = just add this if you want to use the idempotency shit


class PersonResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str | None = None
    age: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
            from_attributes = True
