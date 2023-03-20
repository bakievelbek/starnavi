import datetime

import schemas
import crud
import models

from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Post])
async def read_posts(
        db: Session = Depends(deps.get_db),
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        current_user: models.User = Depends(deps.get_current_user),  # noqa
) -> List[schemas.Post]:
    """
    Fetch list of Posts
    """
    action_data = {"user_id": current_user.id,
                   "action_type": 'Read posts',
                   "created_at": datetime.datetime.now()}
    crud.action.create(db=db, obj_in=action_data)

    return crud.post.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count-by-user", response_model=int)
async def posts_count_per_user(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),  # noqa
) -> Any:
    """
    Fetch list of Posts
    """

    return crud.post.get_count_by_user(db=db, author_id=current_user.id)


@router.get("/{post_id}", response_model=schemas.Post)
async def read_post_by_id(
        post_id: int,
        current_user: models.User = Depends(deps.get_current_user),  # noqa
        db: Session = Depends(deps.get_db)
) -> schemas.Post:
    """
    Get Post by id
    """

    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=404, detail="The post is not found"
        )
    action_data = {"user_id": current_user.id,
                   "action_type": 'Read post',
                   "created_at": datetime.datetime.now()}
    crud.action.create(db=db, obj_in=action_data)
    return post


@router.post("/", response_model=schemas.Post)
async def create_post(
        *,
        db: Session = Depends(deps.get_db),
        post_in: schemas.PostCreate,
        current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Post:
    """
    Create a new Post
    """

    post_in.author_id = current_user.id

    post = crud.post.create(db, obj_in=post_in)

    action_data = {"user_id": current_user.id,
                   "action_type": f'Create post ID - {post.id}',
                   "created_at": datetime.datetime.now()}
    crud.action.create(db=db, obj_in=action_data)

    return post


@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
        *,
        db: Session = Depends(deps.get_db),
        post_id,
        post_in: schemas.PostUpdate,
        current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Post:
    """
    Update a Post
    """
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No Post found")

    if post_in.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="You are not allowed to change another user's post"
        )

    post_in.updated_at = datetime.datetime.now()

    post = crud.post.update(db, db_obj=post, obj_in=post_in)

    action_data = {"user_id": current_user.id,
                   "action_type": f'Update post ID - {post}',
                   "created_at": datetime.datetime.now()}
    crud.action.create(db=db, obj_in=action_data)

    return post


@router.delete("/{post_id}", response_model=schemas.Post)
async def delete_post(
        *,
        db: Session = Depends(deps.get_db),
        post_id: int,
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> schemas.Post:
    post = crud.post.get(db=db, id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No Post found")

    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="You are not allowed to delete another user's post"
        )

    post = crud.post.remove(db=db, id=post_id)

    action_data = {"user_id": current_user.id,
                   "action_type": f'Delete post ID - {post.id}',
                   "created_at": datetime.datetime.now()}
    crud.action.create(db=db, obj_in=action_data)

    return post
