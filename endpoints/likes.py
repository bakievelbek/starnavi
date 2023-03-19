import schemas
import crud
import models

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Like])
async def read_likes(
        db: Session = Depends(deps.get_db),
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> List[schemas.Like]:
    """
    Fetch list of Likes
    """
    return crud.like.get_multi(db=db, skip=skip, limit=limit)


@router.patch("/", response_model=schemas.Like)
async def like_and_unlike(
        like_in: schemas.LikeCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Like:
    """
    Like of unlike post
    """
    post = crud.post.get(db=db, id=like_in.post_id)
    if not post:
        if not post:
            raise HTTPException(
                status_code=404, detail="The post not found"
            )

    like = crud.like.get_by_user_and_post(db=db, user_id=current_user.id, post_id=post.id)
    if not like:
        like_in.user_id = current_user.id
        like = crud.like.create(db, obj_in=like_in)
        return like

    like = crud.like.remove(db=db, id=like.id)

    return like
