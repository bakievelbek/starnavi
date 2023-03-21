import datetime

from crud.base import CRUDBase
from models import Post, Like
from schemas import PostCreate, PostUpdate
from sqlalchemy import func
from sqlalchemy.orm import Session


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_count_by_user(self, db: Session, author_id: int):
        return db.query(self.model).filter(self.model.author_id == author_id).count()

    def get_analytics(self, db: Session, from_date: datetime.date, to_date: datetime.date):
        response = []
        p = {}
        delta = datetime.timedelta(days=1)

        while (from_date <= to_date):
            stmt = db.query(Like.post_id, func.count('*').label('likes_count')).filter(
                Like.created_at < from_date + delta,
                Like.created_at >= from_date).group_by(
                Like.post_id).subquery()

            for post_, count in db.query(self.model, stmt.c.likes_count).outerjoin(stmt,
                                                                                   self.model.id == stmt.c.post_id).order_by(
                self.model.id):
                if count:
                    p['id'] = post_.id
                    p['title'] = post_.title
                    p['num_of_likes'] = count
                    p['date'] = from_date
                    response.append(p)
                    p = {}

            from_date += delta

        return response


post = CRUDPost(Post)
