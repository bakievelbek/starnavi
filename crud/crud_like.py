from crud.base import CRUDBase
from models import Like
from schemas import LikeCreate, LikeUpdate
from sqlalchemy.orm import Session


class CRUDLike(CRUDBase[Like, LikeCreate, LikeUpdate]):
    def get_by_user_and_post(self, db: Session, user_id: int, post_id: int):
        return db.query(self.model).filter(self.model.user_id == user_id, self.model.post_id == post_id).first()

    def get_count_by_post(self, db: Session, post_id: int):
        return db.query(self.model).filter(self.model.post_id == post_id).count()


like = CRUDLike(Like)
