from pydantic import BaseModel, Field


class ChatCreate(BaseModel):
    message: str = Field(max_length=500)


class PersonResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str | None = None
    age: int

    class Config:
        from_attributes = True
