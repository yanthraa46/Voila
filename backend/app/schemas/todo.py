import uuid

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class TodoUpdate(BaseModel):
    completed: bool


class TodoOut(BaseModel):
    id: uuid.UUID
    title: str
    completed: bool

    model_config = {"from_attributes": True}


class TodoDeleteOut(BaseModel):
    success: bool
