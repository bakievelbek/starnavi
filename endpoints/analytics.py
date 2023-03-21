import datetime

import crud
import models

from typing import Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api import deps

router = APIRouter()


@router.get("/likes", response_model=Any)
async def get_likes_data(
        from_date: datetime.date = Query(datetime.date.today()),
        to_date: datetime.date = Query(datetime.date.today()),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> Any:
    """
    Get Analytics about how many likes was made.
    :return: list of posts with post titles, number of likes aggregated by date
    """
    posts = crud.post.get_analytics(db=db, from_date=from_date, to_date=to_date)
    return posts


@router.get("/actions", response_model=Any)
async def get_users_actions(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> Any:
    """
    Get last request to server and last login datetime.
    :return:
    """
    posts = crud.user.get_actions_analytics(db=db)
    return posts
