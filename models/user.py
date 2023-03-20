from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    post = relationship("Post", back_populates="author", cascade="all, delete")
    like = relationship("Like", back_populates="user", cascade="all, delete")
    action = relationship("Action", back_populates="user", cascade="all, delete")
    is_superuser = Column(Boolean(), default=False)
    last_login = Column(DateTime)
