from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="like")
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="like")
    created_at = Column(DateTime, nullable=False)
