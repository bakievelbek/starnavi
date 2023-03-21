import datetime
from typing import Optional, Union, Dict, Any
from crud.base import CRUDBase
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User, Action
from schemas import UserCreate, UserUpdate
from core.security import verify_password, get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        _user = self.get_by_email(db, email=email)
        if not _user:
            return None
        if not verify_password(password, _user.password):
            return None

        _user.last_login = datetime.date.today()
        db.add(_user)
        db.commit()
        db.refresh(_user)
        return _user

    def get_actions_analytics(self, db: Session):
        result = []
        stmt = db.query(Action.user_id, func.max(Action.created_at).label('created_at')).group_by(
            Action.user_id).subquery()

        for user_, created in db.query(self.model, stmt.c.created_at).outerjoin(stmt,
                                                                                self.model.id == stmt.c.user_id).order_by(
            self.model.id):
            user_.__dict__['last_request_datetime'] = created
            print(user_, created)
            result.append(user_)

        return result

    @staticmethod
    def is_active(_user: User) -> bool:
        return _user.is_active

    @staticmethod
    def is_superuser(_user: User) -> bool:
        return _user.is_superuser


user = CRUDUser(User)
