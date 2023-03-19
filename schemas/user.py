from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    password: Optional[str] = None
    is_superuser: Optional[bool] = False


class UserInDBBase(UserBase):
    id: int
    is_superuser: bool

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass
