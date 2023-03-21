from datetime import date
from pydantic import BaseModel
from typing import Optional


class LikeBase(BaseModel):
    post_id: int
    created_at: Optional[date] = date.today()


class LikeCreate(LikeBase):
    user_id: Optional[int] = None


class LikeUpdate(LikeBase):
    pass


class LikeInDBBase(LikeBase):
    id: int

    class Config:
        orm_mode = True


class Like(LikeInDBBase):
    pass
