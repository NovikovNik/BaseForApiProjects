from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    title = Column(String)
    author = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="blogs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    blogs = relationship("Post", back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
