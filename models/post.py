from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="post")
    like = relationship("Like", back_populates="post", cascade="all, delete")
