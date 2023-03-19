import datetime

import crud
import models

from typing import Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api import deps

router = APIRouter()


@router.get("/", response_model=Any)
async def get_data(
        from_date: datetime.datetime = Query(None),
        to_date: datetime.datetime = Query(None),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> Any:
    likes = crud.post.get_analytics(db=db, from_date=from_date, to_date=to_date)
    return likes
