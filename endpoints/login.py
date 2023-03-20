import datetime
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from api import deps
from core import security
from core.config import settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login_access_token(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db=db, email=form_data.username, password=form_data.password
    )

    action_data = {"user_id": user.id, "action_type": 'login', 'created_at': datetime.datetime.now()}
    crud.action.create(db=db, obj_in=action_data)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(subject={"sub": user.email}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
