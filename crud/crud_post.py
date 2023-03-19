import datetime

from crud.base import CRUDBase
from models import Post, Like
from schemas import PostCreate, PostUpdate
from sqlalchemy import func
from sqlalchemy.orm import Session


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_count_by_user(self, db: Session, author_id: int):
        return db.query(self.model).filter(self.model.author_id == author_id).count()

    def get_analytics(self, db: Session, from_date: datetime, to_date: datetime):
        response = []

        stmt = db.query(Like.post_id, func.count('*').label('likes_count')).filter(Like.created_at <= to_date,
                                                                                   Like.created_at >= from_date).group_by(
            Like.post_id).subquery()

        for post_, count in db.query(Post, stmt.c.likes_count).outerjoin(stmt, Post.id == stmt.c.post_id).order_by(
                Post.id):
            post_.__dict__['num_of_likes'] = count
            response.append(post_)

        return response


post = CRUDPost(Post)
