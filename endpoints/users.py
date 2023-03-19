import schemas
import crud
import models

from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(
        db: Session = Depends(deps.get_db),
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> Any:
    """
    Fetch list of Users
    """
    return crud.user.get_multi(db=db, skip=skip, limit=limit)


@router.get("/count", response_model=int)
async def read_users_count(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> Any:
    """
    Fetch number of Users
    """
    return crud.user.get_count(db=db)


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
        user_id: int,
        current_user: models.User = Depends(deps.get_current_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get User by id
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="The user is not found"
        )

    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return user


@router.post("/", response_model=schemas.User)
async def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate
) -> schemas.User:
    """
    Create new User.
    """

    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_user),  # noqa
) -> schemas.User:
    """
    Update a User.
    """
    if user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="You are not allowed to change another user data"
        )

    user = crud.user.get(db, id=user_id)
    if user_id == 1 and current_user.id != 1:
        raise HTTPException(status_code=403, detail="This is super admin")
    if not user:
        raise HTTPException(status_code=404, detail="The user with this username does not exist in the system")
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        current_user: models.User = Depends(deps.get_superuser),  # noqa
) -> schemas.User:
    """
    Delete a User.
    """
    if user_id == 1:
        raise HTTPException(status_code=403, detail="You can't delete superuser")

    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exists")
    user = crud.user.remove(db=db, id=user_id)
    return user
