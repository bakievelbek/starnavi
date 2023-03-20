from datetime import datetime
from pydantic import BaseModel


class ActionBase(BaseModel):
    user_id: int
    created_at: datetime = datetime.now()
    action_type: str


class ActionCreate(ActionBase):
    pass


class ActionUpdate(ActionBase):
    pass


class ActionInDBBase(ActionBase):
    id: int

    class Config:
        orm_mode = True


class Action(ActionInDBBase):
    pass
