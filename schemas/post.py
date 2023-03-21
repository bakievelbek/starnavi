from datetime import date
from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    created_at: Optional[date] = date.today()
    author_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    updated_at: Optional[date] = date.today()


class PostInDBBase(PostBase):
    id: int

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    pass
