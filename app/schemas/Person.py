from pydantic import BaseModel

class PersonCreate(BaseModel):
    last_name: str
    first_name: str
    middle_name: str | None = None
    age: int


class PersonResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str | None = None
    age: int

    class Config:
        from_attributes = True