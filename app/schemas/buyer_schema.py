from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class PersonResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str | None = None
    age: int

    class Config:
        from_attributes = True
