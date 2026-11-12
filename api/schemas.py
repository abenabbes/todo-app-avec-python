from datetime import datetime
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=1000)

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    done: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    created_at: datetime

    class Config:
        from_attributes = True   # permet de convertir un objet SQLAlchemy
